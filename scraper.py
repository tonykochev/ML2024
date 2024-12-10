from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import csv


# Set up Chrome options
options = Options()
#options.add_argument("--headless")  # Run in headless mode (no UI) #error i had to automate, with ui. 
options.add_argument("--disable-gpu")

# Path to your ChromeDriver (make sure it's installed and correctly set up)
service = Service('webdriver/chromedriver.exe')

# Start the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the URL
driver.get("https://asn.flightsafety.org/wikibase/")

# Give time for the page to load, if necessary
driver.implicitly_wait(5)  # Wait up to 5 seconds for elements to load

# Now you can extract the page's HTML using BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

#Find all hyperlinks on the page
links = driver.find_elements(By.TAG_NAME, 'a')

for link in links:
    print(link.get_attribute('href'))

#specify desired years
years=[x for x in range(1950, 2024)]    #(2023 is last year included)

# Open a CSV file in write mode to save the data
with open('avi_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    # Write headers to CSV (modify based on your data)
    writer.writerow(['acc. date', 'type', 'reg.', 'operator', 'fat.', 'location', 'dmg'])  # Adjust columns based on what you're collecting

    #Loop through each link, open it, and extract data
    for link in links:
        href = link.get_attribute('href')
        if href and ('asndb/year' in href) and any(str(year) in href for year in years):    #ensure the link is valid   ()
            print(f"Visiting {href}")

            # Open the link
            driver.get(href)  #ex. https://asn.flightsafety.org/database/year/1950/1

            # Give time for the page to load, if necessary
            driver.implicitly_wait(5)  # Wait up to 5 seconds for elements to load

            # Now you can extract the page's HTML using BeautifulSoup
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extract the table and its rows
            table = soup.find('table', {'class': 'hp'})
            rows = []
            for tr in table.find_all('tr')[1:]:
                cells = tr.find_all('td')
                row = [cell.get_text(strip=True) for cell in cells]
                if row:                                                                 #check if row has () and 3 char string within
                    rows.append(row)

            #write the rows of data to csv file
            for row in rows:
                writer.writerow(row)

            #output
            #print(rows)

            #Go back to the main page to continue to the next link
            driver.back()
            driver.implicitly_wait(5)

# Don't forget to close the WebDriver
driver.quit()

#exit message
print("Scraping complete. Data saved to 'avi_data.csv'.")

#histogram for crashes by year
#geocoding find long and lat from name
#parse use the area codes CDU, SVX
#codes first (they are all airport codes)

#search tool
#city
#add to cart
#view cart download to csv

#weather api
#cut non-code ones out
#between 3 people we can each make 1000 API calls
#be careful may be 3 separate calls to get long lat and then weather
#obtain airport coordinates from airport codes

#https://www.partow.net/miscellaneous/airportdatabase/index.html#Downloads
#last 2 numbers are important

#Tony
#openweather api can get input long and lat for - https://openweathermap.org/
#Yash
#can get long and lat from codes from https://www.partow.net/miscellaneous/airportdatabase/index.html#Downloads

""" import requests
import pandas as pd

API_KEY = 'your_api_key_here'
CITY = 'San Francisco'
DATE = '2023-12-01'

# Step 1: Get latitude and longitude for the city
geo_url = f'http://api.openweathermap.org/geo/1.0/direct?q={CITY}&appid={API_KEY}'
geo_response = requests.get(geo_url).json()
latitude = geo_response[0]['lat']
longitude = geo_response[0]['lon']

# Step 2: Convert date to UNIX timestamp
timestamp = int(pd.Timestamp(DATE).timestamp())

# Step 3: Fetch historical weather data
weather_url = f'https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={latitude}&lon={longitude}&dt={timestamp}&appid={API_KEY}'
weather_response = requests.get(weather_url).json()

# Display the data
print(weather_response) """

#remove ones with no 3 letter code
#remove all 0's in airport data
#final product for airport data should look like screenshot
#use that and time to get weather data
#then can attach the information from api to crash history

#present project next tuesday night (do not have to be there)
#if cannot make it to presentation ask another groupmate to present - one presentation per group