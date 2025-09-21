# 代码生成时间: 2025-09-21 12:57:32
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
def includeme(config):
    # Register views
    config.scan('.views')

def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application. """
    config = Configurator(settings=settings)
    includeme(config)
    return config.make_wsgi_app()

# Views

class ShoppingCart:
    def __init__(self, request):
        """ Initialize the shopping cart with request data. """
        self.request = request
        self.cart_items = []
        # Initialize cart items from session if available
        if 'cart' in self.request.session:
            self.cart_items = self.request.session['cart']
            # Make sure cart_items is a list and convert from JSON if necessary
            if not isinstance(self.cart_items, list):
                try:
                    self.cart_items = [int(item) for item in self.cart_items]
                except ValueError:
                    self.cart_items = []

    def add_item(self, item_id):
        "