import re
import requests
from bs4 import BeautifulSoup

def format_time_elapsed(start_time, elapsed_time):
    total_seconds = elapsed_time.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return hours, minutes, seconds


def print_time_info(start_time, end_time):
    elapsed_time = end_time - start_time
    total_seconds = elapsed_time.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    print("Time elapsed:", hours, "hours,", minutes, "minutes,", seconds, "seconds")


def get_last_page(soup):

    return 1
    # # Find the element containing pagination
    # pagination_element = soup.find('ul', {'data-testid': 'pagination-list'})
    #
    # # Find all page links
    # page_links = pagination_element.find_all('li', {'data-testid': 'pagination-list-item'})
    #
    # # Extract the last page number
    # last_page_number = page_links[-1].get_text(strip=True)
    #
    # # Extract only the number using regular expressions
    # last_page_number = re.search(r'\d+', last_page_number).group()
    #
    # print("Last page number ", last_page_number)
    #
    # return int(last_page_number)


# Function to get the BeautifulSoup object from a URL
def get_soup(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to fetch {url}")
        return None


def get_section_text(html_soup, string, parent_element, next_element):
    # Find the container for the "Wi-Fi and More" section
    section = html_soup.find(parent_element, string=string)

    # Extract the text "Not Included" from the Wi-Fi section if it exists
    text = ''
    if section:
        text = section.find_next(next_element).get_text(strip=True)

    return text


def get_multiple_section_text(soup, section_title):
    section_heading = soup.find('h4', string=section_title)
    text = ''
    if section_heading:
        section_ul = section_heading.find_next('ul')
        if section_ul:
            items = section_ul.find_all('li')
            text = ', '.join(item.get_text(strip=True) for item in items if item.get_text(strip=True))

    print(text)
    return text
