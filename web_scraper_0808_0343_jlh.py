# 代码生成时间: 2025-08-08 03:43:33
# web_scraper.py\
\
"""
A Pyramid web application for scraping web content.
"""\

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from requests import get
from bs4 import BeautifulSoup
from requests.exceptions import RequestException


# Define a custom exception for HTTP errors\
class HTTPError(Exception):
    pass


def get_html_content(url):
    """
    Retrieves the HTML content from the given URL.

    :param url: The URL to fetch the HTML content from.
    :return: The HTML content as a string.
    :raises HTTPError: If the request fails or returns a non-200 status code.
    """
    try:
        response = get(url)
        # Raise an exception if the request was unsuccessful
        response.raise_for_status()
        return response.text
    except RequestException as e:
        raise HTTPError(f"HTTP request failed: {e}")


def parse_html(html_content):
    """
    Parses the HTML content using BeautifulSoup.

    :param html_content: The HTML content to parse.
    :return: The parsed HTML as a BeautifulSoup object.
    """
    return BeautifulSoup(html_content, 'html.parser')

\@view_config(route_name='home', renderer='json')
def home(request):
    """
    The home view that handles scraping a website based on a user's input.

    :param request: The Pyramid request object.
    :return: A JSON response with the scraped content or an error message.
    """
    # Retrieve the URL from the request.params
    url = request.params.get('url')
    if not url:
        return {'error': 'No URL provided'}

    try:
        html_content = get_html_content(url)
        parsed_html = parse_html(html_content)
        # Return the entire HTML content for demonstration purposes
        return {'content': str(parsed_html)}
    except HTTPError as e:
        return {'error': str(e)}


def main(global_config, **settings):
    """
    Configures the Pyramid application.

    :param global_config: The global configuration object.
    :param settings: Additional application settings.
    """
    with Configurator(settings=settings) as config:
        config.add_route('home', '/')
        config.scan()


def run():
    """
    Runs the Pyramid application.
    """
    main({})

if __name__ == '__main__':
    run()