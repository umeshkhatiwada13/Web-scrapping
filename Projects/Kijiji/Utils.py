import re

def format_time_elapsed(start_time, elapsed_time):
    total_seconds = elapsed_time.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    return hours, minutes, seconds


def print_time_info(start_time, end_time):
    elapsed_time = end_time - start_time
    total_seconds = elapsed_time.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = int((total_seconds % 3600) // 60)
    seconds = int(total_seconds % 60)
    print("Time elapsed:", hours, "hours,", minutes, "minutes,", seconds, "seconds")


def get_last_page(soup):
    # Find the element containing pagination
    pagination_element = soup.find('ul', {'data-testid': 'pagination-list'})

    # Find all page links
    page_links = pagination_element.find_all('li', {'data-testid': 'pagination-list-item'})

    # Extract the last page number
    last_page_number = page_links[-1].get_text(strip=True)

    # Extract only the number using regular expressions
    last_page_number = re.search(r'\d+', last_page_number).group()

    print("Last page number ", last_page_number)

    return int(last_page_number)
