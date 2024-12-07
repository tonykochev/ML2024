CREATE DATABASE weather_data;
USE weather_data;

CREATE TABLE weather(
    id INT AUTO_INCREMENT PRIMARY KEY,
    station VARCHAR(20),
    date DATE,
    latitude FLOAT,
    longitude FLOAT,
    elevation FLOAT,
    CDSD FLOAT NULL,
    CLDD FLOAT NULL,
    DP1X FLOAT NULL,
    DT00 FLOAT NULL,
    DX90 FLOAT NULL,
    DYHF FLOAT NULL,
    DYTS FLOAT NULL,
    EMSN FLOAT NULL,
    EMXP FLOAT NULL,
    PRCP FLOAT NULL,
    SNOW FLOAT NULL,
    WSFG FLOAT NULL
);

CREATE USER admin@localhost IDENTIFIED by "abc123";

GRANT SELECT, INSERT, UPDATE, DELETE
ON weather_data.* TO admin@localhost

ALTER TABLE weather
MODIFY COLUMN date YEAR;

/* 
- GHCN: Global Historical Climatology Network - Daily dataset
- "STATION" = GHCN ID
- "DATE" = YYYY-MM where YYYY is 4-digit year and MM is 2-digit month
- "CDSD" = Cooling Degree Days
- "CLDD" = Cooling Degree Days. Computed when daily average temperature is more than 65 degrees
- "DP1X" = Number of days with >= 1.00 inch/25.4 millimeters in the year.
- "DT00" = Number of days with maximum temperature <= 0 degrees Fahrenheit/-17.8 degrees Celsius
- "DX90" = Number of days with maximum temperature >= 90 degrees Fahrenheit/32.2 degrees Celsius
- "DYHF" = Number of Days with Heavy Fog (visibility less than 1/4 statute mile)
- "DYTS" = Number of Days with Thunderstorms
- "EMSN" = Highest daily snowfall in the year. Given in inches or millimeters depending on user specification.
- "EMXP" = Highest daily total of precipitation in the year
- "PRCP" = Total Annual Precipitation.
- "SNOW" = Total Annual Snowfall.
- "WSFG" = Peak Wind Gust Speed
*/
