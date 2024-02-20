from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import numpy as np
import pandas as pd

driver = webdriver.Chrome()
website = 'https://ca.indeed.com/jobs?q=&l=Toronto%2C+ON&fromage=1&vjk=24a0fdea9ecadf02'
driver.get(website)
driver.fullscreen_window()

container = driver.find_element(By.ID, 'mosaic-jobResults')
jobs = container.find_elements(By.XPATH, ".//div[contains(@class, 'job_seen_beacon')]")
print(len(jobs))
wait = WebDriverWait(driver, 10)
# Initialize arrays to store job-related data
title_array = []
company_array = []
location_array = []
description_array = []
error_array = []
benefit_array = []
pay_array = []
job_type_array = []
shift_array = []

# Loop through each job
for job in jobs:
    # Scroll to the job element and click it
    # (Assuming 'driver' is an instance of WebDriver)
    # This allows us to access the details of each job
    driver.execute_script("arguments[0].scrollIntoView();", job)
    child_tag = job.find_element(By.TAG_NAME, 'a')
    child_tag.click()
    time.sleep(2)

    # Find the container for extra job data
    extra_data_container = driver.find_element(By.XPATH, ".//div[contains(@class, 'jobsearch-JobComponent')]")

    # Extract job title and append it to the title array
    title = extra_data_container.find_element(By.XPATH,
                                              ".//h2[contains(@class, 'jobsearch-JobInfoHeader-title')]").text
    title_array.append(title.split("-")[0].strip())

    # Extract company name or NaN if not found, and append it to the company array
    try:
        company = extra_data_container.find_element(By.XPATH, "//div[@data-testid='inlineHeader-companyName']").text
    except NoSuchElementException:
        company = np.nan
    company_array.append(company)

    # Extract job details section
    job_details = extra_data_container.find_elements(By.XPATH,
                                                     "//div[contains(@class, 'js-match-insights-provider-16m282m')]")

    # Initialize flags to track whether data has been appended for each job detail
    appended_pay = False
    appended_job_type = False
    appended_shift = False

    # Loop through job details
    for job_detail in job_details:
        # Extract title and text body for each job detail
        data_head = job_detail.find_element(By.XPATH,
                                            ".//div[contains(@class, 'js-match-insights-provider-e6s05i')]")
        title = data_head.find_element(By.TAG_NAME, "h3").text.lower().replace(" ", '_')
        text_body = data_head.find_elements(By.TAG_NAME, 'li')
        final_text = ', '.join(map(lambda x: x.text, text_body))

        # Append data to the appropriate array based on title
        if title == 'pay' and not appended_pay:
            pay_array.append(final_text)
            appended_pay = True
        elif title == 'job_type' and not appended_job_type:
            job_type_array.append(final_text)
            appended_job_type = True
        elif title == 'shift_and_schedule' and not appended_shift:
            shift_array.append(final_text)
            appended_shift = True

    # If data is not appended for pay_array, job_type_array, or shift_array, append NaN
    if not appended_pay:
        pay_array.append(np.nan)
    if not appended_job_type:
        job_type_array.append(np.nan)
    if not appended_shift:
        shift_array.append(np.nan)

    # Extract job location or NaN if not found, and append it to the location array
    try:
        location = extra_data_container.find_element(By.XPATH, "//div[@data-testid='job-location']").text
    except NoSuchElementException:
        location = np.nan
    location_array.append(location)

    # Extract job description or NaN if not found, and append it to the description array
    try:
        description = extra_data_container.find_element(By.ID, "jobDescriptionText").text.strip()
    except NoSuchElementException:
        description = np.nan
    description_array.append(description)

    # Extract job benefits or NaN if not found, and append it to the benefit array
    try:
        benefits = extra_data_container.find_element(By.ID, 'benefits')
        li_texts = ', '.join(map(lambda li: li.text, benefits.find_elements(By.TAG_NAME, 'li')))
    except NoSuchElementException:
        li_texts = np.nan
    benefit_array.append(li_texts)

# Sleep to ensure all data is loaded before quitting the driver
time.sleep(7)

# Quit the WebDriver
driver.quit()

# Print the length of each array
print("Length of title_array:", len(title_array))
print("Length of company_array:", len(company_array))
print("Length of location_array:", len(location_array))
print("Length of description_array:", len(description_array))
print("Length of error_array:", len(error_array))
print("Length of benefit_array:", len(benefit_array))
print("Length of pay_array:", len(pay_array))
print("Length of job_type_array:", len(job_type_array))
print("Length of shift_array:", len(shift_array))

# Create a DataFrame
data = {
    'Title': title_array,
    'Company': company_array,
    'Location': location_array,
    'Description': description_array,
    # 'Error': error_array,
    'Benefit': benefit_array,
    'Pay': pay_array,
    'Job Type': job_type_array,
    'Shift': shift_array
}

df = pd.DataFrame(data)

df.head()

df.to_csv("indeed.csv", encoding='utf-8', index=False)

# Now you have a DataFrame containing data from the arrays
print("DataFrame Shape:", df.shape)
