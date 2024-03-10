from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time

# URL to scrape
url = "https://www.upwork.com/nx/search/jobs/?page=1&per_page=50&q=machine%20learning&sort=recency"
driver = webdriver.Chrome()

# Open the URL
driver.get(url)

# Wait for the page to fully load
time.sleep(5)

# Wait for the cookie popup to appear
wait = WebDriverWait(driver, 10)
cookie_popup = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "ot-sdk-container")))

# Find and click the "Accept All" button
accept_button = cookie_popup.find_element_by_id('onetrust-accept-btn-handler')
accept_button.click()

# Now, you can proceed with your actions on the page
driver.find_element_by_link_text(title).click()



# Get the page source and parse it with BeautifulSoup
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Find all job postings
jobs = soup.find_all('article', {'class': 'job-tile'})

# Prepare a list to store job data
job_data = []

# Extract relevant info for each job
for job in jobs:
    title_element = job.find('h2', {'class': 'job-tile-title'})
    posted_element = job.find('small', {'class': 'text-light'})
    hourly_element = job.find('li', {'data-test': 'job-type-label'})
    intermediate_element = job.find('li', {'data-test': 'experience-level'})

    # If any of the required fields are not present, skip this job
    if not all([title_element, posted_element, hourly_element, intermediate_element]):
        continue

    title = title_element.text.strip()
    posted = posted_element.text.strip()
    hourly = hourly_element.text.strip()
    intermediate = intermediate_element.text.strip()

    # Check if the 'duration-label' element exists before accessing its text
    est_time_element = job.find('li', {'data-test': 'duration-label'})
    est_time = est_time_element.text.strip() if est_time_element else 'N/A'

    description_element = job.find('p', {'class': 'mb-0'})
    description = description_element.text.strip() if description_element else 'N/A'

    skills = [skill.text.strip() for skill in job.find_all('span', {'class': 'air3-token'})]

    # Find the element based on its partial link text (assuming 'title' contains the partial text)
    element = driver.find_element(By.PARTIAL_LINK_TEXT, title)
    # Click on the element
    element.click()

    # Wait for the popup to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'job-details')))

    # Get the page source of the popup and parse it with BeautifulSoup
    soup_popup = BeautifulSoup(driver.page_source, 'html.parser')

    # Extract the job details from the popup
    job_details = soup_popup.find('div', {'class': 'job-details'})

    # Extract the desired fields from the job details
    # Please replace 'field-name' with the actual class name or other identifier of the field
    job_title = job_details.find('div', {'class': 'field-name'}).text.strip()

    # Add more fields as needed...

    # Store data
    job_data.append([title, posted, hourly, intermediate, est_time, description, skills, job_title])

    # Close the popup
    e2 = driver.find_element(By.CLASS_NAME, 'close-button')
    e2.click()

    # Wait for the popup to close
    time.sleep(2)

# Close the browser
driver.quit()
