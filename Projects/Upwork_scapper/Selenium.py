from bs4 import BeautifulSoup
from selenium import webdriver
import csv
import time

driver = webdriver.Chrome()

# URL to scrape
url = "https://www.upwork.com/nx/search/jobs/?page=1&per_page=50&q=machine%20learning&sort=recency"

# Open the URL
driver.get(url)

# Wait for the page to fully load
time.sleep(5)

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

    # Store data
    job_data.append([title, posted, hourly, intermediate, est_time, description, skills])

# Close the browser
driver.quit()

# Write data to CSV file
with open('jobs.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Title", "Posted", "Hourly", "Intermediate", "Est. Time", "Description", "Skills"])
    writer.writerows(job_data)
