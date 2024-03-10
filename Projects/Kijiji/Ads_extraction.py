import pandas as pd
import requests
from bs4 import BeautifulSoup, PageElement


# Function to get the BeautifulSoup object from a URL
def get_soup(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')
    else:
        print(f"Failed to fetch {url}")
        return None


# Path to the CSV file containing URLs
csv_file_path = 'urls.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(csv_file_path)

df.head()

# Extract the URLs as a list
url_list = df['URL'].tolist()  # Assuming 'URL' is the column containing the URLs

data = []

# Loop through the list of URLs and process each one
for url in url_list:
    print(url)
    soup = get_soup(url)
    if soup:

        # Initialize a dictionary to store the extracted data for this URL
        ad_data = {}

        title_el = soup.find('h1', class_='title-4206718449')
        if title_el is None:
            continue

        # Extract title, price, address, and posting date
        ad_data['Title'] = soup.find('h1', class_='title-4206718449').text.strip()

        # Extract Price
        price_elem = soup.find(class_='priceWrapper-3915768379')
        ad_data['Price'] = price_elem.text.strip() if price_elem else None

        # Extract Address
        address_elem = soup.find(itemprop='address')
        ad_data['Address'] = address_elem.text.strip() if address_elem else None

        # Extract Posting Date
        posting_date_elem = soup.find(class_='datePosted-1776470403')

        # Extract posting date if posting_date_elem is present
        if posting_date_elem:
            ad_data['Posting Date'] = posting_date_elem.time['title']
        else:
            ad_data['Posting Date'] = None

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

        # Extract attributes from Overview section
        overview_section = soup.find('h3', string='Overview')
        if overview_section:
            for li in overview_section.find_next('ul').find_all('li'):
                attribute_title_elem = li.find('h4', class_='attributeGroupTitle-889029213')
                if attribute_title_elem:
                    attribute_title = attribute_title_elem.text.strip()
                    if attribute_title == 'Utilities Included':
                        utilities_included = ', '.join(item.text.strip() for item in li.find('ul').find_all('li'))
                        ad_data['Utilities Included'] = utilities_included
                    elif attribute_title == 'Wi-Fi and More':
                        wifi_included = li.find('ul').text.strip()
                        ad_data['Wi-Fi and More'] = wifi_included
                    elif 'Parking Included' in attribute_title:
                        parking_included = li.find('dd').text.strip()
                        ad_data['Parking Included'] = parking_included
                    elif 'Agreement Type' in attribute_title:
                        agreement_type = li.find('dd').text.strip()
                        ad_data['Agreement Type'] = agreement_type
                    elif 'Pet Friendly' in attribute_title:
                        pet_friendly = li.find('dd').text.strip()
                        ad_data['Pet Friendly'] = pet_friendly

        # Assuming soup is a BeautifulSoup object
        unit_section = soup.find('h3', string='The Unit')
        if unit_section:
            for li in unit_section.find_next('ul').find_all('li'):
                if isinstance(li, PageElement):
                    try:  # Check if li is an instance of PageElement
                        attribute_title_elem = li.find('dt', class_='twoLinesLabel-2332083105')
                        if attribute_title_elem:  # Check if attribute_title_elem is not None
                            attribute_title = attribute_title_elem.text.strip()
                            print('Attribute Title:', attribute_title)
                        else:
                            print('Attribute Title not found.')
                    except Exception as e:
                        print('An error occurred:', e)

        # Extract attributes from The Building section
        building_section = soup.find('h3', string='The Building')
        if building_section:
            for li in building_section.find_next('ul').find_all('li'):
                attribute_title_elem = li.find('dt', class_='twoLinesLabel-2332083105')
                if attribute_title_elem:  # Check if attribute_title_elem is not None
                    attribute_title = attribute_title_elem.text.strip()
                    attribute_value_elem = li.find('dd', class_='twoLinesValue-2653438411')
                    attribute_value = attribute_value_elem.text.strip() if attribute_value_elem else None
                    ad_data[attribute_title] = attribute_value
                else:
                    print('Attribute title not found.')

        # Extract description
        description_elm = soup.select_one('.descriptionContainer-2067035870 p')
        ad_data['Description'] = description_elm.text.strip() if description_elm else None

        # Extract visit counter
        visit_counter_elem = soup.select_one('.visitCounter-204515568 span')
        ad_data['Visit Counter'] = visit_counter_elem.text.strip() if visit_counter_elem else None

        # Extract user info
        user_info_elem = soup.select_one('.container-3136975908 .header-1351916284')
        if user_info_elem:
            ad_data['User Info'] = user_info_elem.text.strip()
        else:
            # Extracting user info from alternative class
            alt_user_info_elem = soup.select_one('.root-3161363123 .header-1351916284')
            ad_data['User Info'] = alt_user_info_elem.text.strip() if alt_user_info_elem else None

        ad_data['url'] = url

        # Append the extracted data to the list
        data.append(ad_data)

    # Create a DataFrame from the collected data
    df = pd.DataFrame(data)

    # Save the DataFrame to a CSV file
    df.to_csv('output.csv', index=False)

    # Display the DataFrame
    print(df)
