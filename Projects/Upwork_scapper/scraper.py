from utils import get_soup_by_selenium_driver


def get_last_page_index(soup):
    div_element = soup.find('div', {'data-ev-max_page_count': True})
    max_page_count = div_element['data-ev-max_page_count']

    return int(max_page_count)


def get_page_urls(url, soup):
    page_urls_list = []
    last_page_index = get_last_page_index(soup)

    for page_num in range(1, last_page_index + 1):
        page_urls_list.append(f'{url}&page={page_num}')

    return page_urls_list


def get_freelancer_details(page_urls):
    freelancers_info = []

    for url in page_urls:
        soup = get_soup_by_selenium_driver(url)
        page_data = soup.find_all('section', class_='flex-1 section')

        for profile_info in page_data:
            name = profile_info.find('h5', class_="name m-0").getText(strip=True).split('.')[0]

            country_name = profile_info.find('h5', class_="name m-0").getText(strip=True).split('.')[1]

            company_name_div = profile_info.find('div', class_='text-base-sm ml-3x')
            if company_name_div:
                company_name_data = company_name_div.getText(strip=True)
                company_name = company_name_data.replace("Associated with", "").strip()
            else:
                company_name = None

            profile_url_element = profile_info.find(
                'h4', class_="title m-0").find('a', class_='up-n-link profile-link')['href']
            profile_url = 'www.upwork.com' + profile_url_element

            profile_image_url = profile_info.find('img', class_="air3-avatar air3-avatar-60")['src']

            company_url_tag = profile_info.find('img', {'data-test': 'FreelancerTileAgencyLogoVue'})
            if company_url_tag:
                company_url_data = company_url_tag['src'].split('/')[-1]
                company_url = 'https://www.upwork.com/agencies/' + company_url_data
            else:
                company_url = None

            job_title = profile_info.find('h4', class_="title m-0").getText(strip=True)

            price_per_hour = profile_info.find('div', {'data-test': 'FreelancerTileRate'}).getText(strip=True)

            job_success_percentage = profile_info.find(
                'div', {'data-test': 'UpCJobSuccessScoreBadge'}).getText(strip=True).split('%')[0]

            earned_amount_element = profile_info.find(
                'span', {'data-test': 'UpCPopover FreelancerTileEarnings'}
            )
            if earned_amount_element:
                earned_amount = earned_amount_element.getText(strip=True).split(' ')[0]
            else:
                earned_amount = None

            company_earned_amount_div = profile_info.find(
                'div', {'class': 'd-flex text-base-sm flex-column align-items-center'}
            )
            if company_earned_amount_div:
                company_earned_amount = company_earned_amount_div.getText(strip=True).split('e')[0]
            else:
                company_earned_amount = None

            description = profile_info.find(
                'div', {'class': 'air3-line-clamp-wrapper mt-4x description text-body'}
            ).getText(strip=True)

            freelancer_info = {
                'name': name,
                'country_name': country_name,
                'company_name': company_name,
                'profile_url': profile_url,
                'profile_image_url': profile_image_url,
                'company_url': company_url,
                'job_title': job_title,
                'price_per_hour': price_per_hour,
                'job_success_percentage': job_success_percentage,
                'earned_amount': earned_amount,
                'company_earned_amount': company_earned_amount,
                'description': description,
            }

            freelancers_info.append(freelancer_info)

    return freelancers_info