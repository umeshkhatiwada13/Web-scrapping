from bs4 import BeautifulSoup
import requests
import string

# Define the root URL and the section for movies starting with letter 'Y'
root = 'https://subslikescript.com'
letter_root = 'movies_letter-Y'

# Define the URL for the main page listing movies starting with letter 'Y'
main_site = f'{root}/{letter_root}'

# Get the content of the main page
result = requests.get(main_site)
content = result.text

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(content, 'lxml')

# Find the pagination section on the main page to determine the number of pages
pagination = soup.find('ul', class_='pagination')

# Extract the second last page link to get the total number of pages
last_page_index = pagination.find_all('a', href=True)[-2]
print(last_page_index.text)

# Initialize a variable to keep track of the total number of movies
total_movies = 0

# Iterate over each page
for page in range(1, int(last_page_index.text) + 1):
    print('Page Number ', page)

    # Get the content of the current page
    result = requests.get(f'{main_site}/?page={page}')
    content = result.text

    # Parse the HTML content of the current page
    soup = BeautifulSoup(content, 'lxml')

    # Find the main article box on the current page
    box = soup.find('article', class_='main-article')

    # Initialize an empty list to store the links of movies on the current page
    link_list = []

    # Extract links of movies from the main article box
    for a in box.find_all('a', href=True):
        link_list.append(a['href'])

    # Print the number of movies on the current page
    print(f'Page {page} Movies number: {len(link_list)}')
    total_movies += len(link_list)

    # Iterate over each movie link on the current page
    for link in link_list:
        try:
            # Get the content of the movie page
            result = requests.get(f'{root}/{link}')
            content = result.text

            # Parse the HTML content of the movie page
            soup = BeautifulSoup(content, 'lxml')

            # Find the main article box on the movie page
            box = soup.find('article', class_='main-article')

            # Extract the transcript text from the full-script div
            transcript = box.find('div', class_='full-script').get_text(strip=True, separator='\n')

            # Extract the title of the movie from the h1 tag
            title = box.find('h1').get_text()

            # Remove any punctuation from the title to avoid filename errors
            title = ''.join(letter for letter in title if letter not in string.punctuation)

            # Write the transcript text to a file with the movie title as the filename
            with open(f'./files/{title}.txt', 'w', encoding='utf8') as file:
                file.write(transcript)
        except Exception as e:
            print("-------- Link not Working --------")
            print(link)
            print(e)
            pass

# Print the total number of movies processed
print("Total Movies ", total_movies)
