# 代码生成时间: 2025-10-07 20:22:46
# atomic_exchange_protocol.py
# This program implements an atomic exchange protocol using the PYRAMID framework.

from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
import threading

"""
Global dictionary to store and exchange values in an atomic way.
"""
_exchange_dict = {}

"""
Class to handle the atomic exchange of values.
"""
class AtomicExchangeProtocol(object):
    def __init__(self):
        self.lock = threading.Lock()

    """
    Store a value in the exchange dictionary.
    :param key: The key to store the value under.
    :param value: The value to store.
    """
    def store(self, key, value):
        with self.lock:
            _exchange_dict[key] = value

    """
    Retrieve a value from the exchange dictionary and replace it with a new value atomically.
    :param key: The key of the value to exchange.
    :param new_value: The new value to replace the old value with.
    :return: The old value.
    """
    def exchange(self, key, new_value):
        with self.lock:
            old_value = _exchange_dict.get(key)
            _exchange_dict[key] = new_value
            return old_value

"""
View function to handle HTTP requests for storing values.
"""
@view_config(route_name='store_value', request_method='POST')
def store_value(request):
    protocol = request.registry.getUtility(AtomicExchangeProtocol)
    key = request.json.get('key')
    value = request.json.get('value')
    try:
        protocol.store(key, value)
        return Response('Value stored successfully.')
    except Exception as e:
        return Response(f'Error storing value: {e}', status=500)

"""
View function to handle HTTP requests for exchanging values.
"""
@view_config(route_name='exchange_value', request_method='POST')
def exchange_value(request):
    protocol = request.registry.getUtility(AtomicExchangeProtocol)
    key = request.json.get('key')
    new_value = request.json.get('new_value')
    try:
        old_value = protocol.exchange(key, new_value)
        return Response(f'Exchanged. Old value: {old_value}')
    except Exception as e:
        return Response(f'Error exchanging value: {e}', status=500)

"""
Main function to setup the Pyramid application and include the views.
"""
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_jinja2')
    config.registry.registerUtility(AtomicExchangeProtocol(), AtomicExchangeProtocol)
    config.add_route('store_value', '/store')
    config.add_route('exchange_value', '/exchange')
    config.scan()
    return config.make_wsgi_app()

if __name__ == '__main__':
    main({})
