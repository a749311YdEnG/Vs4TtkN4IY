# 代码生成时间: 2025-09-13 12:22:34
# system_monitor.py

"""
A simple system performance monitoring tool using Python and Pyramid framework.
"""

from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.httpexceptions import HTTPInternalServerError
import psutil
import logging

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@view_config(route_name='home', renderer='json')
def home(request):
    """
    Home view, returns system performance metrics.
    """
    try:
        # Collect system performance metrics
        cpu_usage = psutil.cpu_percent(interval=1)
        memory_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        # ... Additional metrics can be added here as needed

        # Return the metrics as a JSON response
        return {
            'system': 'ok',
            'cpu_usage': cpu_usage,
            'memory_usage': memory_usage,
            'disk_usage': disk_usage,
        }
    except Exception as e:
        # Log the exception and return an error response
        logger.error(f'Error retrieving system metrics: {e}')
        raise HTTPInternalServerError()

def main(global_config, **settings):
    """
    Pyramid app initialization.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.add_route('home', '/')
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    main()
