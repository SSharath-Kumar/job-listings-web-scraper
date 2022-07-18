# job-listings-web-scraper

 
# Packages used
- Beautiful Soup
  - Installation command - `pip install beautifulsoup4`
- lxml (parser)
  - Installation command - `pip install lxml`
- CSV
- Pandas
- Date Time
- Selenium
  - Installation command - `pip install selenium`
  
# Stage 1 - Web scraping from LinkedIn and Indeed 

## LinkedIn Job Listing Scraper Functions

### linkedin_job_scraper

Input arguments: 
- Job Title
- Location

Returns: `Job List`

The method creates the search string for jobs in LinkedIn. 
Using the generated search string, the response from LinkedIn is then later scraped using the BeautifulSoup library.

The following details are scraped from the response:
- Job title
- Name of the company 
- Location
- Date of posting
- Link to the listing

In case the location parameter contains any spaces or commas, they are converted to URL form using the _set_location_string_ function.

All the above details are packed into a list as rows and returned.

### scroll_and_scrape

Input arguments: `Search URL`

Returns: `Page source code`

The search URL is opened in Chrome using the Chrome webdriver. 
The driver is currently located in the repository but will need to be switched with the appropriate driver on other systems.
Using selenium, the page is scrolled to the bottom. 
Once at bottom, the page source is then extracted and returned 

### draft_csv

Input arguments:
- .csv file name
- list with job details

Returns: `NONE`

If the file exists, it is opened. Else, the file is created.
The file is then read and if empty, headers are added or else, the data is appended to the file.

### sort_csv_data

Input arguments:
- .csv file name

Returns: `NONE`

Using pandas library the csv file is read. The data is then grouped based on the following parameters : company, location and when the job was posted.
After the data is sorted, it is then written into a csv file.

## Indeed Job Listing Scraper Functions

### indeed_job_scraper_setup

Input arguments:
```
Keywords
Location
Page Number
```

Returns: `Beatiful Soup Object`

Similar to the LinkedIn scraper, the search string is built and it's response is used to build the beautiful soup object which is returned.
The _set_location_string_ is once again used to modify the location string passed to match the URL format.

### scraper

Input arguments: `Beatiful Soup Object`

Returns: `None`

The method scrapes the following details from the soup object.
- Job title
- Name of the company 
- Location
- Date of posting
- Link to the listing

All the above details are packed into a dictionary and added onto a global list.

### sort_data

Input arguments: `Job Listings (List)`

Returns: `Data frame with sorted data`

Using the pandas library, the listings are loaded into a dataframe.
This dataframe is then sorted based on the company, location and then returned.
The dataframe is then written to a .csv file.
