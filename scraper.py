from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


# Set up Chrome options
options = Options()
options.add_argument("--headless")  # Run in headless mode (no UI) #error i had to automate, with ui. 
options.add_argument("--disable-gpu")

# Path to your ChromeDriver (make sure it's installed and correctly set up)
service = Service('webdriver/chromedriver.exe')

# Start the WebDriver
driver = webdriver.Chrome(service=service, options=options)

# Open the URL
driver.get("https://asn.flightsafety.org/wikibase/")

#Find all hyperlinks on the page
links = driver.find_elements(By.TAG_NAME, 'a')

#Loop through each link, open it, and extract data
for link in links:
    href = link.get_attribute('href')
    if href:    #ensure the link is valid   ()
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
        if row:
            rows.append(row)

    print(rows)

# Don't forget to close the WebDriver
driver.quit()