import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

web_site = 'https://www.kijiji.ca/b-for-rent/city-of-toronto/c30349001l1700273'
page_number = 1
last_page = 100
ad_url = []


# Function to extract URLs from the current page
def extract_urls(soup):
    # Find all anchor tags with data-testid="listing-link"
    anchor_tags = soup.find_all('a', {'data-testid': 'listing-link'})

    # Extract href attributes from all matching anchor tags
    hrefs = ['https://www.kijiji.ca' + tag.get('href') for tag in anchor_tags]
    return hrefs


def get_last_page(soup):
    # Find the element containing pagination
    pagination_element = soup.find('ul', {'data-testid': 'pagination-list'})

    # Find all page links
    page_links = pagination_element.find_all('li', {'data-testid': 'pagination-list-item'})

    # Extract the last page number
    last_page_number = page_links[-1].get_text(strip=True)

    # Extract only the number using regular expressions
    last_page_number = re.search(r'\d+', last_page_number).group()

    print("Last page number ", last_page_number)

    return int(last_page_number)


# Function to process the current page
def process_page():
    global last_page  # Declare the global variable here
    for page_number in range(1, last_page + 1):
        print("Processing page", page_number)
        site = web_site if page_number == 1 else f'https://www.kijiji.ca/b-for-rent/city-of-toronto/page-{page_number}/c30349001l1700273'
        response = requests.get(site)
        soup = BeautifulSoup(response.text, 'html.parser')

        if page_number == 1:
            print(get_last_page(soup))
            last_page = get_last_page(soup)
            # last_page = 3

        urls = extract_urls(soup)
        ad_url.extend(urls)
    # return ad_url


process_page()

print("Total data ", len(ad_url))

# Create a DataFrame with the URLs
df = pd.DataFrame({'URL': ad_url})

# Specify the file path for the CSV file
csv_file_path = 'urls.csv'

# Save the DataFrame to a CSV file with a header
df.to_csv(csv_file_path, index=False)

print(f"URLs exported to {csv_file_path}")
