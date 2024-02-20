from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import numpy as np

driver = webdriver.Chrome()
website = 'https://ca.indeed.com/jobs?q=&l=Toronto%2C+ON&fromage=1&vjk=24a0fdea9ecadf02'
driver.get(website)
driver.fullscreen_window()

container = driver.find_element(By.ID, 'mosaic-jobResults')
jobs = container.find_elements(By.XPATH, ".//div[contains(@class, 'job_seen_beacon')]")
print(len(jobs))
wait = WebDriverWait(driver, 10)
title_array = []
company_array = []
location_array = []
description_array = []
error_array = []
benefit_array = []
pay_array = []
job_type_array = []
shift_array = []

for job in jobs:
    print("-----------------------------------------------------------------------------------------------")

    # Scroll to the job element (if needed)
    driver.execute_script("arguments[0].scrollIntoView();", job)
    # Click the job element
    child_tag = job.find_element(By.TAG_NAME, 'a')
    child_tag.click()
    time.sleep(2)

    extra_data_container = driver.find_element(By.XPATH, ".//div[contains(@class, 'jobsearch-JobComponent')]")
    # try:
    title = extra_data_container.find_element(By.XPATH,
                                              ".//h2[contains(@class, 'jobsearch-JobInfoHeader-title')]").text

    if title:
        title_array.append(title.split("-")[0])

        try:
            company = extra_data_container.find_element(By.XPATH, "//div[@data-testid='inlineHeader-companyName']").text
        except NoSuchElementException:
            company = np.nan
        company_array.append(company)

        job_details = extra_data_container.find_elements(By.XPATH,
                                                         "//div[contains(@class, 'js-match-insights-provider-16m282m')]")
        for job_detail in job_details:
            data_head = job_detail.find_element(By.XPATH,
                                                ".//div[contains(@class, 'js-match-insights-provider-e6s05i')]")

            title = data_head.find_element(By.TAG_NAME, "h3").text.lower().replace(" ", '_')
            text_body = data_head.find_elements(By.TAG_NAME, 'li')
            final_text = ' '.join(map(lambda x: x.text, text_body))
            print("Title", title)
            for title in text_body:
                print("sub : ", title.text)

            if title == 'pay':
                pay_array.append(final_text)
            elif title == 'job_type':
                job_type_array.append(final_text)
            else:
                shift_array.append(final_text)

        try:
            location = extra_data_container.find_element(By.XPATH, "//div[@data-testid='job-location']").text
        except NoSuchElementException:
            location = np.nan
        location_array.append(location)

        try:
            description = extra_data_container.find_element(By.ID, "jobDescriptionText").text
        except NoSuchElementException:
            description = np.nan
        description_array.append(location)

        try:
            benefits = extra_data_container.find_element(By.ID, 'benefits')
            li_texts = ' '.join(map(lambda li: li.text, benefits.find_elements(By.TAG_NAME, 'li')))
            print("Benefits ", li_texts)
        except NoSuchElementException:
            benefits = np.nan
        benefit_array.append(benefits)

time.sleep(7)

time.sleep(25)

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
