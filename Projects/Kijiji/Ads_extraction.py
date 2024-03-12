import pandas as pd
import requests
from bs4 import BeautifulSoup, PageElement
from datetime import datetime
import re


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


# Path to the CSV file containing URLs
csv_file_path = 'urls.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

df.head()

# Extract the URLs as a list
url_list = df['URL'].tolist()  # Assuming 'URL' is the column containing the URLs

data = []

counter = 1
# Loop through the list of URLs and process each one
for url in url_list:
    # print(url)
    soup = get_soup(url)
    if soup:
        print("Number ", counter, ' and URL ', url)
        # Initialize a dictionary to store the extracted data for this URL
        ad_data = {}

        title_el = soup.find('h1', class_='title-4206718449')
        if title_el is None:
            continue

        # Extract title, price, address, and posting date
        ad_data['Title'] = title_el.text.strip()

        # Extract Price
        price_elem = soup.find(class_='priceWrapper-3915768379')
        price_text = ''
        if price_elem:
            price_text = price_elem.text.strip()
        else:
            backup_price_elem = soup.find(class_='currentPrice-231544276')
            price_text = backup_price_elem.text.strip() if backup_price_elem else None

        ad_data['Price($)'] = ''.join(re.findall(r'\d+', price_text))

        # Extract Address
        address_elem = soup.find(itemprop='address')
        ad_data['Address'] = address_elem.text.strip() if address_elem else None

        # Find the div with class "datePosted"
        date_posted_div = soup.find('div', class_='datePosted-1776470403')

        posted_datetime = ''
        # Extract the datetime attribute from the time tag
        if date_posted_div:
            time_tag = date_posted_div.find('time')
            if time_tag and 'datetime' in time_tag.attrs:
                datetime_str = time_tag['datetime']

                # Parse the datetime string into a datetime object
                posted_datetime = datetime.strptime(datetime_str, "%Y-%m-%dT%H:%M:%S.%fZ")

        ad_data['Date Posted'] = posted_datetime

        # Extract bedrooms, bathrooms, and building type if title_attributes is present
        title_attributes = soup.find(class_='titleAttributes-183069789')
        if title_attributes:
            title_attributes = title_attributes.find_all('li', class_='noLabelAttribute-262950866')
            for attr in title_attributes:
                if 'Bedrooms' in attr.span.text:
                    ad_data['Bedrooms'] = attr.span.text.split(': ')[-1]
                elif 'Bathrooms' in attr.span.text:
                    ad_data['Bathrooms'] = attr.span.text.split(': ')[-1]
                else:
                    ad_data['Building Type'] = attr.span.text

        # Handle case where title_attributes is not present
        else:
            ad_data['Bedrooms'] = None
            ad_data['Bathrooms'] = None
            ad_data['Building Type'] = None

        # Find the container for the "Utilities Included" section
        utilities_included_container = soup.find('h4', string='Utilities Included')

        # Extract the "Utilities Included" section if it exists
        utilities_text = ''
        if utilities_included_container:
            utilities_included_section = utilities_included_container.find_next('ul')
            if utilities_included_section:
                utilities_element = utilities_included_section.find_all('li')
                utilities_text = ','.join(
                    f"{item.get_text(strip=True)}_Yes" if 'Yes' in item.find('svg').get('aria-label',
                                                                                        '') else f"{item.get_text(strip=True)}_No" if 'No' in item.find(
                        'svg').get('aria-label', '') else f"{item.get_text(strip=True)}" for item in utilities_element)

        # Print the combined text with Yes/No indicators
        ad_data['Utilities'] = utilities_text

        # Get and print each section's text
        ad_data['Wi-Fi and More'] = get_section_text(soup, 'Wi-Fi and More', 'h4', 'ul')

        ad_data['Parking Included'] = get_section_text(soup, 'Parking Included', 'dt', 'dd')

        ad_data['Agreement Type'] = get_section_text(soup, 'Agreement Type', 'dt', 'dd')

        ad_data['Move-In Date'] = get_section_text(soup, 'Move-In Date', 'dt', 'dd')

        ad_data['Pet Friendly'] = get_section_text(soup, 'Pet Friendly', 'dt', 'dd')

        ad_data['Size (sqft)'] = get_section_text(soup, 'Size (sqft)', 'dt', 'dd')

        ad_data['Furnished'] = get_section_text(soup, 'Furnished', 'dt', 'dd')

        ad_data['Air Conditioning'] = get_section_text(soup, 'Air Conditioning', 'dt', 'dd')

        ad_data['Personal Outdoor Space'] = get_section_text(soup, 'Personal Outdoor Space', 'h4', 'ul')

        ad_data['Smoking Permitted'] = get_section_text(soup, 'Smoking Permitted', 'dt', 'dd')

        ad_data['Appliances'] = get_multiple_section_text(soup, 'Appliances')
        ad_data['Amenities'] = get_multiple_section_text(soup, 'Amenities')

        # Extract description
        description_elm = soup.select_one('.descriptionContainer-2067035870 p')
        ad_data['Description'] = description_elm.text.strip() if description_elm else None

        # Extract visit counter
        visit_counter_elem = soup.select_one('.visitCounter-204515568 span')
        ad_data['Visit Counter'] = visit_counter_elem.text.strip() if visit_counter_elem else None

        ad_data['url'] = url

        # Append the extracted data to the list
        data.append(ad_data)

        counter += 1

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_csv('output.csv', index=False)
