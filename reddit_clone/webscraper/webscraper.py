from datetime import datetime

import psycopg2
import requests
from bs4 import BeautifulSoup as bs


# webscraping tech crunch
def get_webpage(url: str):
    """Creates a BeautifulSoup object for a given URL

    Args:
        url (str): URL for a webpage

    Returns:
        soup: BeautifulSoup object of webpage
    """
    webpage_response = requests.get(url)
    webpage = webpage_response.content
    soup = bs(webpage, "html.parser")
    return soup

# what to put into the database

# stories: title, url, created_at, updated_at

# scrape: title, url, author, created_at

def filter_soup(*class_ids):
    pass

def get_title(soup):
    pass

def get_url(soup):
    pass

def get_author(soup):
    pass

def get_created_date(soup):
    pass


if __name__ == "__main__":
    tech_crunch_url = "https://techcrunch.com/"
    tech_crunch_soup = get_webpage(tech_crunch_url)
    print(tech_crunch_soup)
