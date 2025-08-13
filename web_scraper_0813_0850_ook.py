# 代码生成时间: 2025-08-13 08:50:42
import requests
from bs4 import BeautifulSoup
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

"""
Web Scraper Pyramid Application

This application provides a simple web scraper tool to fetch and display
content from a specified URL.

@author: Your Name
@version: 1.0
"""

# Define a function to scrape the content of a webpage
def scrape_webpage(url):
    try:
        # Send a GET request to the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors

        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        return soup.prettify()  # Return the formatted HTML content
    except requests.exceptions.RequestException as e:
        # Handle exceptions related to the request
        return f"Error fetching URL: {e}"
    except Exception as e:
        # Handle any other exceptions
        return f"An error occurred: {e}"

# Create a Pyramid view to handle the scraping request
@view_config(route_name='scrape', renderer='json')
def scrape_view(request):
    # Get the URL from the request parameters
    url = request.params.get('url')

    # Check if the URL is provided
    if not url:
        return Response(json_body={'error': 'URL parameter is missing'}, content_type='application/json', status=400)

    # Scrape the webpage content
    scraped_content = scrape_webpage(url)

    # Return the scraped content as JSON
    return {'content': scraped_content}

# Configure the Pyramid application
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.add_route('scrape', '/scrape')
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    server = make_server('0.0.0.0', 6543, main)
    server.serve_forever()