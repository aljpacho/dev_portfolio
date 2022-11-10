# TODO: 
# put all relevant information into a dictionary
# apply dictionary to all in soup using for loop
# populate database
# test that is comes up on the frontend

from datetime import datetime

import psycopg2
import requests
from bs4 import BeautifulSoup as bs

POST_BLOCK_CLASS = "post-block__header"
AUTHOR_CLASS = "river-byline__authors"

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
    filtered_soup = soup.find_all(attrs={"class": class_attr})
    return filtered_soup


def get_title(filtered_soup_element) -> str:
    """Returns the title from an HTML <a> tag

    Args:
        filtered_soup_element: an element from a BeautifulSoup object

    Returns:
        title: the text for a title
    """
    title_a_tag = filtered_soup_element.a
    title = title_a_tag.get_text().strip()
    return title


def get_url(filtered_soup_element) -> str:
    """Returns the URL associated with a story

    Args:
        filtered_soup_element: an element from a BeautifulSoup object

    Returns:
        url: the url for a story
    """
    url_a_tag = filtered_soup_element.a
    url = url_a_tag["href"]
    return url


def get_author(filtered_soup_element) -> str:
    """Returns the author associated with a story

    Args:
        filtered_soup_element: an element from a BeautifulSoup object

    Returns:
        author: the author for a story
    """
    author_elements = filtered_soup_element.find(attrs={"class": AUTHOR_CLASS})
    author = author_elements.get_text()
    return author


def get_created_date(filtered_soup_element) -> datetime:
    """Returns the created date with timezone for a story

    Args:
        filtered_soup_element: an element from a BeautifulSoup object

    Returns:
        datetime_parsed: datetime object with timezone
    """
    datetime_element = filtered_soup_element.time.attrs["datetime"]
    datetime_parsed = datetime.fromisoformat(datetime_element)
    return datetime_parsed




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
        print(f"{get_created_date(obj)}\n\n")
