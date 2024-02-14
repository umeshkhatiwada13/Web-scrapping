from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
import time

# define the website url
website = 'https://www.adamchoi.co.uk/overs/detailed'

# initialize the chrome webdriver
driver = webdriver.Chrome()

# open the website in browser
driver.get(website)

# Record the start time
start_time = time.time()

# click on the 'All matches' button
all_match_button = driver.find_element(By.XPATH, "//label[@analytics-event='All matches']")
all_match_button.click()

# Click on the 'All matches' button
all_match_button = driver.find_element(By.XPATH, "//label[@analytics-event='All matches']")
all_match_button.click()

dropdown = Select(driver.find_element(By.ID, 'country'))

options = dropdown.options

total_rows = 0
total_files_created = 0
country_wise_rows = {}
for index, option in enumerate(options[0:3]):
    print(f"Scrapping data for {option.text} with index {index}")
    dropdown.select_by_index(index)

    # wait for 2 seconds for google.com to load (way 1)
    time.sleep(2)

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
    df.to_csv(f'Scraped_data/{option.text}_pl_data.csv', index=False)

    total_rows = total_rows + len(date)
    total_files_created = total_files_created + 1
    country_wise_rows[option.text] = len(date)

# Record the end time
end_time = time.time()

# Close the webdriver
driver.quit()

# Calculate the total time elapsed
total_time_seconds = end_time - start_time
total_time_minutes = total_time_seconds / 60

# Print the total time elapsed
print("Total time elapsed (seconds): ", total_time_seconds)
print("Total time elapsed (minutes): ", total_time_minutes)
print("Total rows scrapped: ", total_rows)
print("Total Files created in System: ", total_files_created)
print("Country wise rows count: ", country_wise_rows)
