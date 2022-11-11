from datetime import datetime

import requests
from bs4 import BeautifulSoup as bs

import webscraper_to_db

POST_BLOCK_CLASS = "post-block__header"
AUTHOR_CLASS = "river-byline__authors"
TECH_CRUNCH_URL = "https://techcrunch.com/"


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


"""Implement after finishing mvp"""
# def get_author(filtered_soup_element) -> str:
#     """Returns the author associated with a story

#     Args:
#         filtered_soup_element: an element from a BeautifulSoup object

#     Returns:
#         author: the author for a story
#     """
#     author_elements = filtered_soup_element.find(attrs={"class": AUTHOR_CLASS})
#     author = author_elements.get_text().strip("\n")
#     return author


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


def create_story_dictionary(filtered_soup_element) -> dict:
    """Creates a dictionary with key:value pairs for
    title, author, url, and created_at

    Args:
        filtered_soup_element (_type_): _description_

    Returns:
        dict: _description_
    """

    story = {
        "title": get_title(filtered_soup_element),
        "url": get_url(filtered_soup_element),
        "created_at": get_created_date(filtered_soup_element),
    }

    return story


def generate_stories(url=TECH_CRUNCH_URL) -> list:
    """Generates a list of dictionaries with key:value pairs
    for title, author, url, and created_at

    Args:
        url (Defaults to TECH_CRUNCH_URL)

    Returns:
        stories: list of story dictionaries
    """
    html_soup = get_webpage(url)
    filtered_soup = filter_soup(html_soup)
    stories = [create_story_dictionary(story) for story in filtered_soup]
    return stories


if __name__ == "__main__":
    stories = generate_stories()
    db_connection = webscraper_to_db.DBConnection()
    db_connection.add_stories(stories)
