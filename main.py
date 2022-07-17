import requests
import csv
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup


def linkedin_job_scraper(title, location):
    # title = "Software Developer"
    # location = "Texas"

    # Building the search string
    search_string = 'https://www.linkedin.com/jobs/search?'
    title_string = "keywords=" + title.replace(" ", "%20")
    location_string = "&location=" + location.replace(" ", "%20")
    end_string = "&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&position=1&pageNum=0"
    final_search_string = search_string + title_string + location_string + end_string
    print('SEARCH STRING ', final_search_string)

    # Get the response web page
    html_response = requests.get(final_search_string).text
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

        # Create a row with all details and add to main list
        row = [job_title, company_name, location, posted_date, link_to_listing, today]
        job_list.append(row)

        # Displaying info -> Building purpose only
        # print(f"Job Title: {job_title}")
        # print(f"Company Name: {company_name}")
        # print(f"Location: {location}")
        # print(f"Posted on: {posted_date}")
        # print(f"Link to listing: {link_to_listing}")
        # print("-------------")
    return job_list


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
            fields = ['Job Title', 'Company', 'Location', 'Posted On', 'Link to posting', 'Date Scraped']
            csv_writer.writerow(fields)
        csv_writer.writerows(listings)


def sort_csv_data(csv_file_name):
    data = pd.read_csv(csv_file_name)
    data.sort_values(["Company", "Location", "Posted On"], axis=0, inplace=True)
    data.to_csv('LinkedIn_Listings.csv')


if __name__ == "__main__":
    file = 'temp.csv'
    job_listings = linkedin_job_scraper('Software Developer', 'Texas')
    draft_csv(file, job_listings)
    sort_csv_data(file)

