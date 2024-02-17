from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
# Import pandas library
import pandas as pd

# Create Chrome options with headless mode
headless_config = Options()
headless_config.add_argument("--headless=new")
headless_config.add_argument('--window-size=1920x1080')  # Set window size

# Initialize the Chrome driver
driver = webdriver.Chrome(options=headless_config)


def separate_rating(rating_string):
    # Check if the string is empty or contains "Not rated yet"
    if not rating_string or "Not rated yet" in rating_string:
        return None, None  # Return None for both values
    # Split the string by newline character
    lines = rating_string.split("\n")
    # Get the first line and remove the " out of 5 stars" part
    avg_rating = lines[0].replace(" out of 5 stars", "")
    # Convert the average rating to a float
    avg_rating = float(avg_rating)
    # Get the second line and remove the " ratings" part
    num_rating = lines[1].replace(" ratings", "").replace(" rating", '').replace(",", '')
    # Convert the number of ratings to an int
    num_rating = int(num_rating)
    # Return the average rating and the number of ratings as a tuple
    return avg_rating, num_rating


website = "https://www.audible.ca/search "

# driver = webdriver.Chrome(options=headless_config)

driver.get(website)
# driver.maximize_window()

container = driver.find_element(By.CLASS_NAME, 'adbl-impression-container')
products = container.find_elements(By.XPATH, './/li[contains(@class, "productListItem")]')

# Create empty lists to store each data
titles = []
authors = []
narrators = []
runtimes = []
release_dates = []
languages = []
avg_ratings = []
rating_count = []

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
