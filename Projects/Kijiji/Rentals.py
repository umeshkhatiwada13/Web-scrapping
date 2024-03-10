from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import time
import numpy as np
import pandas as pd
import re
import requests
from bs4 import BeautifulSoup
import re

# driver = webdriver.Chrome()
website = 'https://www.kijiji.ca/b-for-rent/city-of-toronto/c30349001l1700273'
# driver.get(website)
# driver.fullscreen_window()

# Send an HTTP GET request to the page
response = requests.get(website)

# # Find the element containing pagination
# pagination_element = driver.find_element(By.XPATH, "//ul[@data-testid='pagination-list']")
#
# # Find all page links
# page_links = pagination_element.find_elements(By.XPATH, ".//li[@data-testid='pagination-list-item']")
#
# # Extract the last page number
# last_page_number = page_links[-1].text.strip()
#
# # Extract only the number using regular expressions
# last_page_number = re.search(r'\d+', last_page_number).group()
#
# print(last_page_number)

# for i in range()


# Parse the HTML content of the page
soup = BeautifulSoup(response.text, 'html.parser')

# Find the element containing pagination
pagination_element = soup.find('ul', {'data-testid': 'pagination-list'})

# Find all page links
page_links = pagination_element.find_all('li', {'data-testid': 'pagination-list-item'})

# Extract the last page number
last_page_number = page_links[-1].get_text(strip=True)

# Extract only the number using regular expressions
last_page_number = re.search(r'\d+', last_page_number).group()

print("Last page number ", last_page_number)

# Close the WebDriver
# driver.quit()
