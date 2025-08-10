# 代码生成时间: 2025-08-10 08:56:50
# web_scraper.py

"""
A Pyramid web application that provides a web content scraping tool.
This tool allows users to input a URL and retrieves the HTML content of the page.
"""

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup


# Define a custom error class for invalid URLs
class InvalidURLException(Exception):
    pass


# Define a function to check if a URL is valid
def is_valid_url(url):
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False


# Define a function to scrape content from a given URL
def scrape_content(url):
    if not is_valid_url(url):
        raise InvalidURLException("The provided URL is invalid.")
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"An error occurred while fetching the page: {e}"


# Create a Pyramid view to handle the scraping request
@view_config(route_name='scrape', renderer='json')
def scrape_view(request):
    """
    A Pyramid view that handles scraping requests.
    It takes a URL from the request and returns the HTML content of the page.
    """
    url = request.params.get('url')
    if url:
        content = scrape_content(url)
        return {'status': 'success', 'content': content}
    else:
        return {'status': 'error', 'message': 'No URL provided.'}


# Configure the Pyramid application
def main(global_config, **settings):
    """
    Configure the Pyramid WSGI application.
    This function sets up the routes and views for the application.
    """
    with Configurator(settings=settings) as config:
        config.add_route('scrape', '/scrape')
        config.scan()


if __name__ == '__main__':
    main({})