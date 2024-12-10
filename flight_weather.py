from sqlalchemy import create_engine
import pandas as pd

# Load flight accident data
accidents = pd.read_csv("merged.csv")

# Convert 'acc. date' to datetime and extract the year
accidents['acc. date'] = pd.to_datetime(accidents['acc. date'], format="%d %b %Y")
accidents['year'] = accidents['acc. date'].dt.year

# Create SQLAlchemy engine and query weather data
query = "SELECT * FROM weather;"
with create_engine("mysql+mysqlconnector://admin:abc123@localhost/weather_data").connect() as connection:
    weather = pd.read_sql(query, connection)

# Rename and round latitude and longitude
accidents.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'}, inplace=True)
weather.rename(columns={'Latitude': 'latitude', 'Longitude': 'longitude'}, inplace=True)
accidents['latitude'] = accidents['latitude'].round(0)
accidents['longitude'] = accidents['longitude'].round(0)
weather['latitude'] = weather['latitude'].round(0)
weather['longitude'] = weather['longitude'].round(0)

# Extract year from weather data if needed
weather['date'] = pd.to_datetime(weather['date']).dt.year

# Merge datasets
merged_data = pd.merge(
    accidents,
    weather,
    left_on=['year', 'latitude', 'longitude'],
    right_on=['date', 'latitude', 'longitude'],
    how='inner'  # Change to 'left' or 'outer' if necessary
)

# Preview the merged dataset
print(merged_data.head())

# Drop irrelevant columns and ensure target column is numeric
merged_data = merged_data.drop(columns=['acc. date', 'year', 'date'])
merged_data['fat.'] = pd.to_numeric(merged_data['fat.'], errors='coerce').fillna(0)

merged_data.to_csv("weather_flights.csv", index=False)
# Final preview
print(merged_data)
