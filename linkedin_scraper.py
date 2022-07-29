import os
import time
import csv
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup
from pandas import CategoricalDtype
from selenium import webdriver

output_path = os.getcwd() + '\\output\\'


def set_location_string(location):
    loc_url_string = location
    if " " in location:
        loc_url_string = loc_url_string.replace(" ", "%20")
    if "," in location:
        loc_url_string = loc_url_string.replace(",", "%2C")
    return loc_url_string


def linkedin_job_scraper(keywords, location):
    # title = "Software Developer"
    # location = "Texas"

    # Building the search string
    search_string = 'https://www.linkedin.com/jobs/search?'
    keyword_string = "keywords=" + keywords.replace(" ", "%20")
    location_string = "&location=" + set_location_string(location)
    end_string = "&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0"
    final_search_string = search_string + keyword_string + location_string + end_string
    # print('LINKEDIN SEARCH STRING: ', final_search_string)

    # Get the response web page
    html_response = scroll_and_scrape(final_search_string)
    # html_response = requests.get(final_search_string).text # Needs import requests
    soup = BeautifulSoup(html_response, 'html.parser')
    '''
    # Initial scraping
    results = soup.find_all('div', class_='base-card relative w-full hover:no-underline focus:no-underline '
                                       'base-card--link base-search-card base-search-card--link '
                                       'job-search-card')
    '''
    results = soup.find('ul', class_="jobs-search__results-list")
    jobs = results.find_all('li')

    # Placeholder list
    job_list = []

    for job in jobs:
        # Extracting details
        job_title = job.find('h3', class_="base-search-card__title").text.strip()
        company_name = job.find('h4', class_="base-search-card__subtitle").text.strip()
        location = job.find('span', class_="job-search-card__location").text.strip()
        posted_date = job.find('time').text.strip()
        link_to_listing = job.find('a')['href']
        today = date.today()

        # Filtering Jobs
        if 'Volunteer' in job_title:
            continue

        # Create a row with all details and add to main list
        row = [today, job_title, company_name, location, posted_date, link_to_listing]
        job_list.append(row)

        # Displaying info -> Building purpose only
        # print(f"Job Title: {job_title}")
        # print(f"Company Name: {company_name}")
        # print(f"Location: {location}")
        # print(f"Posted on: {posted_date}")
        # print(f"Link to listing: {link_to_listing}")
        # print("-------------")
    return job_list


def scroll_and_scrape(url):
    webdriver_path = os.getcwd() + "\\web-drivers\\chromedriver.exe"
    driver = webdriver.Chrome(webdriver_path)
    driver.get(url)
    driver.maximize_window()
    while True:
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight);")
        time.sleep(7)
        current_page = driver.page_source
        soup = BeautifulSoup(current_page, 'html.parser')
        see_more = soup.find('button', class_="infinite-scroller__show-more-button "
                                              "infinite-scroller__show-more-button--visible")
        if see_more is not None:
            driver.close()
            break
    return current_page


def draft_csv(csv_file_name, listings):
    with open(csv_file_name, 'w+', newline='') as csv_file:
        # Setting up writer
        csv_writer = csv.writer(csv_file)

        # Check if csv file is empty
        csv_reader = csv.reader(csv_file)
        line_count = 0
        for line in csv_reader:
            if line is not None:
                line_count += 0
        if line_count == 0:
            fields = ['Date scraped', 'Job Title', 'Company', 'Location', 'Posted On', 'Link to listing']
            csv_writer.writerow(fields)
        csv_writer.writerows(listings)


def sort_csv_data(csv_file_name):
    df = pd.read_csv(csv_file_name, encoding='unicode_escape')

    cat_order_list = ['1 minute ago']
    for m in range(2, 60):
        cat_order_list.append(f'{m} minutes ago')
    cat_order_list.append('1 hour ago')
    for h in range(2, 24):
        cat_order_list.append(f'{h} hours ago')
    cat_order_list.append('1 day ago')
    for d in range(2, 7):
        cat_order_list.append(f'{d} days ago')
    cat_order_list.append('1 week ago')
    for w in range(2, 5):
        cat_order_list.append(f'{w} weeks ago')
    cat_order_list.append('1 month ago')
    for m in range(2, 12):
        cat_order_list.append(f'{m} months ago')

    cat_order = CategoricalDtype(cat_order_list, ordered=True)
    df['Posted On'] = df['Posted On'].astype(cat_order)
    # Sort rows based on company and posting date
    df.sort_values(["Company", "Posted On"], axis=0, inplace=True)
    df.to_csv(output_path + 'LinkedIn_Listings.csv', index=False)
    os.remove(csv_file_name)


def scrape_init(title, location):
    file = output_path + 'temp.csv'
    job_listings = linkedin_job_scraper(title, location)
    draft_csv(file, job_listings)
    sort_csv_data(file)
