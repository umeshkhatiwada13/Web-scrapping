import pandas as pd

from scraper import get_page_urls, get_freelancer_details
from utils import get_soup_by_selenium_driver

user_url = input('Please type a url: ')

soup = get_soup_by_selenium_driver(user_url)
page_urls = get_page_urls(user_url, soup)
freelancer_details = get_freelancer_details(page_urls)

df = pd.DataFrame(freelancer_details)
df.to_excel(f'freelancer_data.xlsx', index=False, engine='xlsxwriter')