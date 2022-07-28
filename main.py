import indeed_scraper
import linkedin_scraper


if __name__ == "__main__":
    title = 'Software Developer'
    location = 'Texas'
    indeed_scraper.scrape_init(title, location)
    linkedin_scraper.scrape_init(title, location)
