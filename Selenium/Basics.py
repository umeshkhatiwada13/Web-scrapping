from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pandas as pd

website = 'https://www.adamchoi.co.uk/overs/detailed'
driver = webdriver.Chrome()

driver.get(website)

all_match_button = driver.find_element(By.XPATH, "//label[@analytics-event='All matches']")
all_match_button.click()

matches = driver.find_elements(By.TAG_NAME, 'tr')

date = []
home_team = []
score = []
away_team = []
for match in matches:
    # index starts from 1 in xpath
    date.append(match.find_element(By.XPATH, './td[1]').text)
    home_team.append(match.find_element(By.XPATH, './td[2]').text)
    score.append(match.find_element(By.XPATH, './td[3]').text)
    away_team.append(match.find_element(By.XPATH, './td[4]').text)

df = pd.DataFrame({'Date': date, "Home team": home_team, 'Score': score, 'Away team': away_team})
df.to_csv('Scraped_data/football_pl_data.csv', index=False)

driver.quit()
