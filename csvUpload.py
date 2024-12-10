import os
import pandas as pd
import mysql.connector

# MySQL connection setup
conn = mysql.connector.connect(
    host="localhost",
    user="admin",
    password="abc123",
    database="weather_data"
)
cursor = conn.cursor()

# Path to the folder containing CSV files
csv_folder_path = "/Users/tonykochev/Desktop/School/Fall 2024/Machine Learning /Final Project/ML2024/gsoy-latest"

# Function to upload filtered data to MySQL
def upload_filtered_data(file_path, table_name):
    # Define required columns based on the database schema
    required_columns = ['STATION', 'DATE', 'LATITUDE', 'LONGITUDE', 'ELEVATION',
                        'CDSD', 'CLDD', 'DP1X', 'DT00', 'DX90', 'DYHF', 'DYTS',
                        'EMSN', 'EMXP', 'PRCP', 'SNOW', 'WSFG']
    
    # Load CSV into a DataFrame
    df = pd.read_csv(file_path)

    # Ensure all required columns are present, adding missing ones with None
    for col in required_columns:
        if col not in df:
            df[col] = None  # Add missing column with None (NULL for MySQL)

    # Ensure the 'DATE' column only contains valid years
    if 'DATE' in df.columns:
        df['DATE'] = df['DATE'].apply(lambda x: int(x) if pd.notnull(x) else None)

    # Keep only required columns, drop extras
    df = df[required_columns]

    # Replace NaN with None for MySQL compatibility
    df = df.where(pd.notnull(df), None)

    # Convert the DataFrame to a list of tuples for database insertion
    data = df.values.tolist()

    # Define the SQL query
    placeholders = ', '.join(['%s'] * len(required_columns))
    sql = f"""
    INSERT INTO {table_name} 
    ({', '.join(required_columns)}) 
    VALUES ({placeholders})
    """

    # Insert data into the database
    cursor.executemany(sql, data)
    conn.commit()
    print(f"Uploaded {len(data)} rows from {file_path} to {table_name}")

# Iterate through all CSV files and upload filtered data
for file_name in os.listdir(csv_folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(csv_folder_path, file_name)
        try:
            upload_filtered_data(file_path, "weather")
        except mysql.connector.errors.ProgrammingError as e:
            print(f"Error uploading {file_name}: {e}")
        except Exception as e:
            print(f"Unexpected error uploading {file_name}: {e}")

# Close the cursor and connection
cursor.close()
conn.close()
