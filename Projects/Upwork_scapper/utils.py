import time

from bs4 import BeautifulSoup
from selenium import webdriver


def get_soup_by_selenium_driver(url):
    driver = webdriver.Chrome()
    driver.get(url)
    time.sleep(5)

    soup = BeautifulSoup(driver.page_source, 'html.parser')

    return soup