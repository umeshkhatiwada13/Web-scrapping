import requests
from bs4 import BeautifulSoup

# URL of the "Saved Jobs" page on Upwork
upwork_url = "https://www.upwork.com/nx/find-work/saved-jobs"

# Set headers to mimic a browser request
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# Send an HTTP request to the Upwork page with headers
response = requests.get(upwork_url, headers=headers)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract information based on HTML structure
    # Example: Extracting job titles
    job_titles = [title.text.strip() for title in soup.select('.job-title')]

    # Print the extracted job titles
    print("Job Titles:")
    print(job_titles)

    # Add similar code to extract other information such as descriptions, hourly rates, etc.

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")