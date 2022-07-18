import requests
import pandas as pd
from datetime import date
from bs4 import BeautifulSoup


def set_location_string(location):
    loc_url_string = location
    if " " in location:
        loc_url_string = loc_url_string.replace(" ", "%20")
    if "," in location:
        loc_url_string = loc_url_string.replace(",", "%2C")
    return loc_url_string


def indeed_job_scraper_setup(keywords, location, page):
    # Building the search string
    search_string = "https://www.indeed.com/jobs?"
    keyword_string = "q=" + keywords.replace(" ", "+")
    location_string = "&l=" + set_location_string(location)
    end_string = f"&from=searchOnHP&redirected=0&start={page}"
    final_search_string = search_string + keyword_string + location_string + end_string
    # print(f'INDEED SEARCH STRING: {final_search_string}')

    # Get the response web page
    html_response = requests.get(final_search_string).text
    soup = BeautifulSoup(html_response, 'html.parser')
    return soup


def scraper(soup):
    place_holder_url = 'www.indeed.com'
    divs = soup.find_all('div', class_='job_seen_beacon')
    for listing in divs:
        job_title = listing.find('a').text.strip()
        company = listing.find('span', class_='companyName').text.strip()
        location = listing.find('div', class_='companyLocation').text.strip()
        posted_on = listing.find('span', class_='date').text.strip()
        posted_on = posted_on.replace('Posted', '')
        link_to_listing = place_holder_url + listing.find('a')['href']
        today = date.today()
        job = {
            'Date scraped': today,
            'Job Title': job_title,
            'Company': company,
            'Location': location,
            'Posted On': posted_on,
            'Link to listing': link_to_listing
        }
        job_listings.append(job)


def sort_data(listings):
    df = pd.DataFrame(listings)
    df.sort_values(['Company', 'Location'], axis=0, inplace=True)
    return df


if __name__ == "__main__":
    job_listings = []
    for i in range(0, 190, 10):
        indeed_soup = indeed_job_scraper_setup('Software Developer', 'Texas', i)
        scraper(indeed_soup)
    data = sort_data(job_listings)
    file = 'Indeed_Listings.csv'
    data.to_csv(file)
