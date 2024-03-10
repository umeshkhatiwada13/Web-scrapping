from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.chrome.options import Options

from selenium import webdriver

PROXY = '190.205.32.70'

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f"--proxy-server={PROXY}")

chrome_options = Options()
# chrome_options.add_argument("--disable-extensions")
# chrome_options.add_argument("--disable-gpu")
# chrome_options.add_argument("--no-sandbox") # linux only
chrome_options.add_argument("--headless=new") # for Chrome >= 109
# chrome_options.add_argument("--headless")
# chrome_options.headless = True # also works
driver = webdriver.Chrome(options=chrome_options)


# URL to scrape
url = "https://www.upwork.com/nx/search/jobs/?page=1&per_page=20&q=machine&sort=recency"

# Open the URL
driver.get(url)

# Wait for the page to fully load
time.sleep(5)

# # Check if the cookie popup is present
# try:
#     cookie_popup = WebDriverWait(driver, 5).until(
#         EC.visibility_of_element_located((By.CLASS_NAME, "ot-sdk-container"))
#     )
#
#     # If the cookie popup is present, click the "Close" button
#     close_button = cookie_popup.find_element(By.CLASS_NAME, "onetrust-close-btn-handler")
#     close_button.click()
#
# except Exception as e:
#     # If the cookie popup is not present or there's an error, print the exception
#     print("Error handling cookie popup:", e)

# Find all job articles
job_articles = driver.find_elements(By.XPATH, "//article[@data-test='JobTile']")

# Iterate through each job article
for job_article in job_articles:
    # Click on the job title
    job_title = job_article.find_element(By.CLASS_NAME, "job-tile-title")
    job_title_text = job_title.text
    job_title.click()

    # Handle the popup here (code to close the popup, extract information, etc.)
    try:
        # Wait for the popup to appear
        popup = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "popup-class"))
        )

        # Code to handle the popup

        # Close the popup
        close_button = popup.find_element(By.CLASS_NAME, "close-button")
        close_button.click()

    except Exception as e:
        print("Error handling popup:", e)

# Navigate back to the main page
driver.back()

# # Write data to CSV file
# with open('jobs.csv', 'w', newline='', encoding='utf-8') as file:
#     writer = csv.writer(file)
#     writer.writerow(["Title", "Posted", "Hourly", "Intermediate", "Est. Time", "Description", "Skills"])
#     writer.writerows(job_data)
