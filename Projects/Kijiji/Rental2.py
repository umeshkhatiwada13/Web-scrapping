from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

# Initialize the WebDriver (assuming you have Chrome WebDriver installed)
driver = webdriver.Chrome()

# Load the initial page
driver.get("https://www.kijiji.ca/b-for-rent/city-of-toronto/c30349001l1700273")


# Function to extract URLs from the current page
def extract_urls(soup):
    # Find all anchor tags with data-testid="listing-link"
    anchor_tags = soup.find_all('a', {'data-testid': 'listing-link'})

    # Extract href attributes from all matching anchor tags
    hrefs = ['https://www.kijiji.ca/' + tag.get('href') for tag in anchor_tags]
    return hrefs


# Function to process the current page
def process_page(driver):
    # Get the page source
    page_source = driver.page_source
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(page_source, 'html.parser')
    # Extract URLs from the current page
    urls = extract_urls(soup)
    # Process the URLs (you can store them or do further processing)
    for url in urls:
        print("URL:", url)


# Function to click the next button
def click_next(driver):
    try:
        # Find and click the next button
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[contains(@title, 'Next')]"))
        )
        next_button.click()
        return True
    except:
        return False


# Process the initial page
process_page(driver)

# Loop through pages until there's no next button
while click_next(driver):
    # Add a delay to avoid overwhelming the server
    time.sleep(5)
    # Process the current page
    process_page(driver)

print()

# Close the WebDriver
driver.quit()
