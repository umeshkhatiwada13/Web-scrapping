from bs4 import BeautifulSoup
import requests

# define website
website = 'https://subslikescript.com/movie/Titanic-120338'
# get result back from website
result = requests.get(website)
content = result.text

soup = BeautifulSoup(content, 'lxml')

box = soup.find('article', class_='main-article')
title = box.find('h1').get_text()

transcript = box.find('div', class_='full-script').get_text(strip=True, separator=' ')

with open(f'{title}.txt', 'w', encoding='utf8') as file:
    file.write(transcript)
