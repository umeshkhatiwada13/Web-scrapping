import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
import Utils


# Function to extract URLs from the current page
def extract_urls(soup):
    # Find all anchor tags with data-testid="listing-link"
    anchor_tags = soup.find_all('a', {'data-testid': 'listing-link'})

    # Extract href attributes from all matching anchor tags
    hrefs = ['https://www.kijiji.ca' + tag.get('href') for tag in anchor_tags]
    return hrefs


# Function to process the current page
def process_page():
    start_time = datetime.now()
    global last_page  # Declare the global variable here
    for page_number in range(1, last_page + 1):
        print("Processing page", page_number)
        site = web_site if page_number == 1 else f'https://www.kijiji.ca/b-for-rent/city-of-toronto/page-{page_number}/c30349001l1700273'
        response = requests.get(site)
        soup = BeautifulSoup(response.text, 'html.parser')

        if page_number != 1:
            response = requests.get(site)
            soup = BeautifulSoup(response.text, 'html.parser')

        urls = extract_urls(soup)
        ad_url.extend(urls)
    end_time = datetime.now()
    Utils.print_time_info(start_time, end_time)
    # return ad_url


web_site = 'https://www.kijiji.ca/b-city-of-toronto/apartment/k0l1700273?dc=true&sort=dateDesc'
page_number = 1
ad_url = []

# Fetch the first page
response = requests.get(web_site)
soup = BeautifulSoup(response.text, 'html.parser')
# Calculate the last page dynamically
last_page = Utils.get_last_page(soup)

print(last_page)

process_page()

print("Total data ", len(ad_url))

# Create a DataFrame with the URLs
df = pd.DataFrame({'URL': ad_url})

# Specify the file path for the CSV file
csv_file_path = 'kijiji_rental_ads_url.csv'

# Save the DataFrame to a CSV file with a header
df.to_csv(csv_file_path, index=False)

print(f"URLs exported to {csv_file_path}")
