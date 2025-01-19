import requests
from bs4 import BeautifulSoup
import csv
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Configure Selenium WebDriver (make sure ChromeDriver is installed)
chrome_options = Options()
chrome_options.add_argument("--headless")  # Run headless browser
service = Service(executable_path='/path/to/chromedriver')  # Set correct path to ChromeDriver
driver = webdriver.Chrome(service=service, options=chrome_options)

# URL to scrape
url = "https://sscasn.bkn.go.id/"

# Step 1: Scraping static content using Requests and BeautifulSoup
def scrape_static_content():
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'lxml')
        # Example: Scraping all headings and links
        headings = soup.find_all(['h1', 'h2', 'h3'])
        links = soup.find_all('a')
        print("Headings:")
        for heading in headings:
            print(heading.text)
        print("\nLinks:")
        for link in links:
            print(f"{link.text}: {link.get('href')}")
    else:
        print(f"Failed to retrieve the page. Status code: {response.status_code}")

# Step 2: Scraping dynamic content with Selenium
def scrape_dynamic_content():
    driver.get(url)
    time.sleep(2)  # Wait for the page to load fully
    # Example: Scraping specific dynamic content
    elements = driver.find_elements(By.TAG_NAME, 'h1')
    for element in elements:
        print(element.text)
    
    # Example: Click a button or interact with the page
    # button = driver.find_element(By.ID, "exampleButtonID")
    # button.click()
    # time.sleep(2)  # Wait for the next page or new content to load

# Step 3: Handling paginated data (if applicable)
def scrape_paginated_data():
    driver.get(url)
    time.sleep(2)
    
    # Example: Assuming there is a "Next" button to click for pagination
    while True:
        try:
            # Scrape data from the current page
            elements = driver.find_elements(By.CLASS_NAME, 'pagination-item')
            for element in elements:
                print(element.text)
            
            # Click the "Next" button for pagination
            next_button = driver.find_element(By.XPATH, "//a[contains(text(), 'Next')]")
            if next_button:
                next_button.click()
                time.sleep(2)  # Wait for the next page to load
            else:
                break  # No more pages
        except Exception as e:
            print(f"Error during pagination: {e}")
            break

# Step 4: Saving scraped data to CSV (or other formats)
def save_data_to_csv(data, filename="output.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Heading", "Link"])  # Example headers
        for row in data:
            writer.writerow(row)

# Main function to execute scraping
def main():
    print("Scraping static content...")
    scrape_static_content()
    
    print("\nScraping dynamic content...")
    scrape_dynamic_content()
    
    print("\nScraping paginated content (if applicable)...")
    scrape_paginated_data()
    
    # Example: Save data to CSV
    # data = [['Heading 1', 'https://example.com'], ['Heading 2', 'https://example2.com']]
    # save_data_to_csv(data)

if __name__ == "__main__":
    main()

    # Close the Selenium driver when done
    driver.quit()
