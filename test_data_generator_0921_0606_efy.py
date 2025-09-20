# 代码生成时间: 2025-09-21 06:06:50
# test_data_generator.py

"""
A Pyramid application that acts as a test data generator.
"""

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import random
import string

# Utility functions

def generate_random_string(length=10):
    """Generate a random string of fixed length."""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def generate_random_number():
    """Generate a random number between 1 and 1000.""""
    return random.randint(1, 1000)


def generate_test_data():
    """Generate a dictionary with random test data.""""
    return {
        'id': generate_random_string(5),
        'name': generate_random_string(10),
        'age': generate_random_number(),
        'active': random.choice([True, False])
    }

# Pyramid view
@view_config(route_name='generate_test_data', renderer='json')
def generate_test_data_view(request):
    """
    Endpoint to generate and return test data.
    """
    try:
        test_data = generate_test_data()
        return test_data
    except Exception as e:
        return Response(f"Error generating test data: {e}", status=500)

# Pyramid application setup
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    with Configurator(settings=settings) as config:
        config.include('.pyramid route setup')
        config.add_route('generate_test_data', '/test_data')
        config.scan()
    return config.make_wsgi_app()
