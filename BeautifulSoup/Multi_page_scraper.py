from bs4 import BeautifulSoup
import requests

# Define the root URL
root = 'https://subslikescript.com'

# Define the main page URL
website = f'{root}/movies'

# Get the content of the main page
result = requests.get(website)
content = result.text

# Parse the HTML content
soup = BeautifulSoup(content, 'lxml')

# Find the main article box on the main page
box = soup.find('article', class_='main-article')

# Initialize an empty list to store the links
link_list = []

# Extract links from the main article box
for a in box.find_all('a', href=True):
    link_list.append(a['href'])

# Print the list of links
print(link_list)

# Iterate over a subset of links (e.g., the first 3 links)
for link in link_list[2:4]:
    # Define the website URL for each movie
    website = f'{root}/{link}'

    # Get the content of the movie page
    result = requests.get(website)
    content = result.text

    # Parse the HTML content of the movie page
    soup = BeautifulSoup(content, 'lxml')

    # Find the main article box on the movie page
    box = soup.find('article', class_='main-article')

    # Extract the transcript text from the full-script div
    transcript = box.find('div', class_='full-script').get_text(strip=True, separator='\n')

    # Extract the title of the movie from the h1 tag
    title = box.find('h1').get_text()

    # Write the transcript text to a file with the movie title as the filename
    with open(f'{title}.txt', 'w', encoding='utf8') as file:
        file.write(transcript)
