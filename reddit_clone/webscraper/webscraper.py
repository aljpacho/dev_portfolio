from datetime import datetime

import psycopg2
import requests
from bs4 import BeautifulSoup as bs

POST_BLOCK_CLASS = "post-block__header"

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

def filter_soup(soup, class_attr=POST_BLOCK_CLASS) -> list:
    """Filter BeautifulSoup object by a given class attribute

    Args:
        soup: BeautifulSoup object 
        class_attr (str, optional): HTML class attribute. Defaults to POST_BLOCK_CLASS.

    Returns:
        filtered_soup: a list of all elements that include the class_attr
    """
    filtered_soup = soup.find_all(attrs={"class":  class_attr})
    return filtered_soup

def get_title(filtered_soup_element) -> str:
    """Returns the title from an HTML <a> tag

    Args:
        filtered_soup_element: an element from a BeautifulSoup object

    Returns:
        title: the text for a title
    """
    title_link_tag = filtered_soup_element.a
    title = title_link_tag.get_text().strip()
    return title

def get_url(filtered_soup):
    pass

def get_author(filtered_soup):
    pass

def get_created_date(filtered_soup):
    pass


if __name__ == "__main__":
    tech_crunch_url = "https://techcrunch.com/"
    tech_crunch_soup = get_webpage(tech_crunch_url)


    filtered_soup = filter_soup(tech_crunch_soup)

    # for i, obj in enumerate(filtered_soup):
    #     print(f"Object {i} \n \n")
    #     print(f"\n {obj} \n")
    #     print('\n \n')

    for i, obj in enumerate(filtered_soup):
        print(f"Story {i} \n\n")
        print(f"{get_title(obj)}\n\n")
        
