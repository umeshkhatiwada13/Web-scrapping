import requests
import csv
from bs4 import BeautifulSoup

def extract_jobs(page_number, keyword):
    base_url = "https://www.upwork.com/nx/search/jobs/"
    params = {
        "page": page_number,
        "per_page": 50,
        "q": keyword,
        "sort": "recency",
    }
    response = requests.get(base_url, params=params)
    soup = BeautifulSoup(response.content, "html.parser")

    job_listings = []
    for job in soup.find_all("div", class_="job-tile"):
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

# Keywords to search
keywords = ["machine learning", "data science", "artificial intelligence", "deep learning", "data analytics"]

# Extract jobs for each keyword
all_jobs = []
for keyword in keywords:
    print(f"Extracting jobs for keyword: {keyword}")
    for page_num in range(1, 51):
        all_jobs.extend(extract_jobs(page_num, keyword))

# Save data to a CSV file
csv_filename = "upwork_jobs_keywords.csv"
with open(csv_filename, "w", newline="") as csvfile:
    fieldnames = ["Title", "Company", "Location", "Job URL"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for job in all_jobs:
        writer.writerow(job)

print(f"Data saved to {csv_filename}")
