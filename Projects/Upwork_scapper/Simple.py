import requests
from bs4 import BeautifulSoup

def extract_jobs(page_number):
    base_url = "https://www.upwork.com/nx/search/jobs/"
    params = {
        "page": page_number,
        "per_page": 50,
        "q": "machine learning",
        "sort": "recency",
    }
    response = requests.get(base_url, params=params)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")

    job_listings = []
    for job in soup.find_all("div", class_="job-tile"):
        print(job)
        title = job.find("h2").text.strip()
        company = job.find("span", class_="client-name").text.strip()
        location = job.find("span", class_="client-location").text.strip()
        job_url = job.find("a", class_="job-title-link")["href"]

        job_info = {
            "Title": title,
            "Company": company,
            "Location": location,
            "Job URL": job_url,
        }
        job_listings.append(job_info)

    return job_listings

# Extract jobs from pages 1 to 50
all_jobs = []
for page_num in range(1, 51):
    all_jobs.extend(extract_jobs(page_num))

# Print the extracted job information
for job in all_jobs:
    print(f"Title: {job['Title']}")
    print(f"Company: {job['Company']}")
    print(f"Location: {job['Location']}")
    print(f"Job URL: {job['Job URL']}")
    print("-" * 40)

# You can save this data to a file or process it further as needed.
