# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Define the website URL
website = 'https://www.adamchoi.co.uk/overs/detailed'

# Initialize the Chrome webdriver
driver = webdriver.Chrome()

# Open the website in the browser
driver.get(website)

# Click on the 'All matches' button
all_match_button = driver.find_element(By.XPATH, "//label[@analytics-event='All matches']")
all_match_button.click()

# Find all elements with tag 'tr' (table rows) representing matches
matches = driver.find_elements(By.TAG_NAME, 'tr')

# Initialize lists to store match data
date = []
home_team = []
score = []
away_team = []

# Iterate over each match row to extract data
for match in matches:
    # Extract data from each column (td) of the current match row
    date.append(match.find_element(By.XPATH, './td[1]').text)
    home_team.append(match.find_element(By.XPATH, './td[2]').text)
    score.append(match.find_element(By.XPATH, './td[3]').text)
    away_team.append(match.find_element(By.XPATH, './td[4]').text)

# Create a DataFrame from the extracted data
df = pd.DataFrame({'Date': date, "Home team": home_team, 'Score': score, 'Away team': away_team})

# Save the DataFrame to a CSV file
df.to_csv('Scraped_data/football_pl_data.csv', index=False)

# Close the webdriver
driver.quit()
