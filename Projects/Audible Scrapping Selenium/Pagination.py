from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
# Import pandas library
import pandas as pd
import time

# Create Chrome options with headless mode
headless_config = Options()
# headless_config.add_argument("--headless=new")
# headless_config.add_argument('--window-size=1920x1080')  # Set window size

# Initialize the Chrome driver
driver = webdriver.Chrome(options=headless_config)


def separate_rating(rating_string):
    # Check if the string is empty or contains "Not rated yet"
    if not rating_string or "Not rated yet" in rating_string:
        return None, None  # Return None for both values
    # Split the string by newline character
    lines = rating_string.split("\n")
    print(lines)
    # Get the first line and remove the " out of 5 stars" part
    avg_rating = lines[0].replace(" out of 5 stars", "")
    print(avg_rating)
    # Convert the average rating to a float
    avg_rating = float(avg_rating)
    # Get the second line and remove the " ratings" part
    num_rating = lines[1].replace(" ratings", "").replace(" rating", '').replace(",", '')
    print(num_rating)
    # Convert the number of ratings to an int
    num_rating = int(num_rating)
    # Return the average rating and the number of ratings as a tuple
    return avg_rating, num_rating


website = "https://www.audible.ca/search?node=21073392011&publication_date=20971902011&ref_pageloadid=dOFFwUF1fYWVBrZk&ref=a_search_l1_publication_date_2&pf_rd_p=e73bc6dd-0441-4a91-9b45-0da1b5c2a70a&pf_rd_r=1E40AN4DVDWNQXJVNG4N&pageLoadId=KTuKkG10UIqB7lVw&creativeId=9648f6bf-4f29-4fb4-9489-33163c0bb63e"

# driver = webdriver.Chrome(options=headless_config)

driver.get(website)
driver.maximize_window()

pagination = driver.find_element(By.XPATH, "//ul[contains(@class, 'pagingElements')]")
pages = pagination.find_elements(By.TAG_NAME, 'li')
page_number = 1
last_page = int(pages[-2].text)

print("Last page ", last_page)

# Create empty lists to store each data
titles = []
authors = []
narrators = []
runtimes = []
release_dates = []
languages = []
avg_ratings = []
rating_count = []
while page_number < last_page:
    # explicit wait
    time.sleep(2)

    # implicit wait
    # container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container')
    # products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')

    # explicit wait
    # wait 5 seconds until the given element renders in DOM
    container = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'adbl-impression-container')))
    products = WebDriverWait(driver, 5).until(
        EC.presence_of_all_elements_located((By.XPATH, './/li[contains(@class, "productListItem")]')))

    # Loop over each product list item and append the data to the lists
    for product in products:
        titles.append(product.find_element(By.XPATH, ".//h3[contains(@class,'bc-heading')]/a").text)
        authors.append(product.find_element(By.XPATH, ".//li[contains(@class,'authorLabel')]").text)
        # Remove the "Narrated by: " prefix from the narrator text
        narrators.append(product.find_element(By.XPATH, ".//li[contains(@class,'narratorLabel')]")
                         .text.replace("Narrated by: ", ""))
        # Remove the "Length: " prefix from the runtime text
        runtimes.append(product.find_element(By.XPATH, ".//li[contains(@class,'runtimeLabel')]")
                        .text.replace("Length: ", ""))
        # Remove the "Release date: " prefix from the release date text
        release_dates.append(product.find_element(By.XPATH, ".//li[contains(@class,'releaseDateLabel')]")
                             .text.replace("Release date: ", ""))
        # Remove the "Language: " prefix from the language text
        languages.append(product.find_element(By.XPATH, ".//li[contains(@class,'languageLabel')]")
                         .text.replace("Language: ", ""))
        # Remove the " out of 5 stars" suffix from the ratings text
        ratings = product.find_element(By.XPATH, ".//li[contains(@class,'ratingsLabel')]").text
        avg_rating, rating = separate_rating(ratings)
        avg_ratings.append(avg_rating)
        rating_count.append(rating)

    page_number = page_number + 1

    try:
        next_page = driver.find_element(By.XPATH, "//span[contains(@class,'nextButton')]")
        next_page.click()
    except:
        pass

# Create a pandas dataframe from the lists
df = pd.DataFrame({
    "Title": titles,
    "Author": authors,
    "Narrator": narrators,
    "Runtime": runtimes,
    "Release Date": release_dates,
    "Language": languages,
    "Average Rating": avg_ratings,
    "Total rating": rating_count
})

# Display the dataframe
df.head()

# Export the dataframe to audiobooks.csv with no index
df.to_csv("audiobooks.csv", index=False)

driver.quit()
