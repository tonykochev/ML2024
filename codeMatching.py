import csv
import re
import pandas as pd

# Function to find 3-letter capital airport codes and preserve acc. date and fat.
def find_capital_letters_with_details(csv_file, column_name):
    result = []
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            text = row[column_name]
            matches = re.findall(r'\(([A-Z]{3})\)', text)
            if matches:
                # Append extracted code along with acc. date and fat. 
                for match in matches:
                    result.append({
                        'Extracted_Code': match,
                        'acc. date': row['acc. date'],
                        'fat.': row['fat.']
                    })
    return result

# File and column to extract the airport codes
csv_file = 'avi_data.csv'  
column_name = 'location'  

# Extracted codes along with acc. date and fat.
extracted_data = find_capital_letters_with_details(csv_file, column_name)

# Convert the extracted data into a DataFrame
avi_data = pd.DataFrame(extracted_data)

# Check the first few rows of avi_data to confirm
print("Extracted Data with acc. date and fat.:\n", avi_data.head())

# Load the airports data (this should contain airport codes, etc.)
airports_data = pd.read_csv("airports-code@public.csv", sep=";")
airports_data['Airport Code'] = airports_data['Airport Code'].str.strip().str.upper()

# Merge the extracted data with airports data based on the extracted airport code
merged_data = pd.merge(
    avi_data,
    airports_data,
    left_on='Extracted_Code',
    right_on='Airport Code',
    how='inner'
)

# Print the merged data to verify the result
print("Merged Data with acc. date, fat., and airport info:\n", merged_data[['Extracted_Code', 'acc. date', 'fat.', 'Airport Code', 'Longitude', 'Latitude']])

# Optionally, save the filtered results to a new CSV
merged_data[['Extracted_Code', 'acc. date', 'fat.', 'Airport Code', 'Longitude', 'Latitude']].to_csv("merged.csv", index=False)
