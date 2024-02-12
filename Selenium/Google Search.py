from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.google.com")

# wait for 2 seconds for google.com to load (way 1)
time.sleep(2)

WebDriverWait(driver, 2).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'gLFyf'))
)

# find search box
search_box = driver.find_element("name", "q")
search_box.send_keys("Umeshkhatiwada13")

search_box.send_keys(Keys.RETURN)

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located((By.TAG_NAME, "h3"))
) 

link = driver.find_element(By.TAG_NAME, "h3")
link.click()

time.sleep(5)
driver.quit()
