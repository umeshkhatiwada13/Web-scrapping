import requests
from bs4 import BeautifulSoup
import csv
from selenium import webdriver


def fetch_job_info(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract job information
    job_title = soup.find('h4').text.strip()
    posted_time = soup.find('div', {'data-test': 'PostedOn'}).text.strip().replace('Posted', '')
    location = soup.find('span', class_='text-light-on-muted').text.strip()

    # Extract job description
    job_description = soup.find('div', {'data-test': 'Description'}).p.text.strip()

    # Extract budget
    budget = soup.find('div', {'data-test': 'BudgetAmount'}).strong.text.strip()

    # Extract experience level
    experience_level = soup.find('div', text='Experience Level').find_next('strong').text.strip()

    # Extract remote job status
    remote_job = soup.find('strong', text='Remote Job').text.strip()

    # Extract project type
    project_type = soup.find('strong', text='Project Type').text.strip()

    # Extract skills and expertise
    skills_list = [skill.text.strip() for skill in soup.find_all('span', {'data-test': 'Skill'})]

    # Extract client activity
    proposals = soup.find('span', text='Proposals:').find_next('span').text.strip()
    last_viewed = soup.find('span', text='Last viewed by client:').find_next('span').text.strip()

    # Extract about the client
    member_since = soup.find('small').text.strip()

    # Extract additional information
    interviewing = soup.find('strong', text='Interviewing:').find_next('span').text.strip()
    invites_sent = soup.find('strong', text='Invites sent:').find_next('span').text.strip()
    unanswered_invites = soup.find('strong', text='Unanswered invites:').find_next('span').text.strip()
    hiring_location = soup.find('strong', text='Location:').find_next('span').text.strip()
    hiring_time = soup.find('strong', text='Time:').find_next('span').text.strip()
    jobs_posted = soup.find('strong', text='Jobs posted').find_next('span').text.strip()
    hire_rate = soup.find('strong', text='Hire rate').find_next('span').text.strip()
    total_spent = soup.find('strong', text='Total spent').find_next('span').text.strip()
    hires = soup.find('strong', text='Hires').find_next('span').text.strip()
    active_jobs = soup.find('strong', text='Active').find_next('span').text.strip()
    company_name = soup.find('strong', text='Company name').find_next('span').text.strip()

    return {
        'job_title': job_title,
        'posted_time': posted_time,
        'location': location,
        'job_description': job_description,
        'budget': budget,
        'experience_level': experience_level,
        'remote_job': remote_job,
        'project_type': project_type,
        'skills_list': skills_list,
        'proposals': proposals,
        'last_viewed': last_viewed,
        'member_since': member_since,
        'interviewing': interviewing,
        'invites_sent': invites_sent,
        'unanswered_invites': unanswered_invites,
        'hiring_location': hiring_location,
        'hiring_time': hiring_time,
        'jobs_posted': jobs_posted,
        'hire_rate': hire_rate,
        'total_spent': total_spent,
        'hires': hires,
        'active_jobs': active_jobs,
        'company_name': company_name
    }


def save_to_csv(job_data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = job_data[0].keys()
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(job_data)


def main():
    # Set up Selenium WebDriver
    driver = webdriver.Chrome()  # Assuming you have Chrome WebDriver installed. You can use other drivers as well.

    # Define the URL
    url = 'https://www.upwork.com/nx/search/jobs/?page=1&per_page=50&q=machine%20learning&sort=recency'

    # Fetch job info
    job_data = fetch_job_info(url)

    # Save data to CSV
    save_to_csv(job_data, 'jobs_info.csv')

    # Close the WebDriver
    driver.quit()


if __name__ == "__main__":
    main()
