# 代码生成时间: 2025-08-11 21:12:54
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
import random

def generate_random_number(min_value, max_value):
    """Generates a random number between the given minimum and maximum values.

    Args:
        min_value (int): The minimum value of the random number range.
        max_value (int): The maximum value of the random number range.

    Returns:
        int: A random number between min_value and max_value.
    """
    if min_value >= max_value:
        raise ValueError("Minimum value must be less than maximum value.")
    return random.randint(min_value, max_value)

@view_config(route_name='random_number', renderer='json')
def random_number_view(request):
    """View function to handle requests for generating a random number.

    Args:
        request: The Pyramid request object.

    Returns:
        Response: A Pyramid response object with a JSON body containing the random number.
    """
    try:
        min_value = request.params.get("min", 0)
        max_value = request.params.get("max", 100)
        min_value = int(min_value)
        max_value = int(max_value)
        random_number = generate_random_number(min_value, max_value)
        return {"random_number": random_number}
    except ValueError as e:
        return Response(status=400, body=str(e), content_type="text/plain")

def main(global_config, **settings):
    """Main function to set up the Pyramid application.

    Args:
        global_config (dict): Global configuration dictionary.
        **settings: Additional settings.
    """
    config = Configurator(settings=settings)
    config.add_route('random_number', '/random_number')
    config.scan()
    return config.make_wsgi_app()
