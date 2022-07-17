# job-listings-web-scraper

 
# Packages used
- Beautiful Soup
  - Installation command - `pip install beautifulsoup4`
- lxml (parser)
  - Installation command - `pip install lxml`
- CSV
- Pandas
- Date Time

# Stage 1 - Web scraping from LinkedIn

## Functions

### linkedin_job_scraper

Input arguments: 
- Job Title
- Location

Returns:
- Job List

The method creates the search string for jobs in LinkedIn. 
Using the generated search string, the response from LinkedIn is then later scraped using the BeautifulSoup library.

The following details are scraped from the response:
- Job title
- Name of the company 
- Location
- Date of posting
- Link to the listing

The above details are packed into a list as rows and returned.

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
