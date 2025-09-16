# 代码生成时间: 2025-09-17 02:04:29
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.request import Request
from collections import defaultdict

LOG = None  # Placeholder for a logging instance

# Define the ShoppingCart class
class ShoppingCart:
    def __init__(self):
        self.cart = defaultdict(list)

    def add_product(self, request, product_id, quantity):
        """Add a product to the cart."""
        if quantity > 0:
            self.cart[product_id].append(quantity)
            request.session['cart'] = dict(self.cart)
        else:
            raise ValueError("Quantity must be greater than 0.")

    def remove_product(self, request, product_id):
        """Remove a product from the cart."""
        if product_id in self.cart:
            del self.cart[product_id]
            request.session['cart'] = dict(self.cart)
        else:
            raise KeyError("Product not found in cart.")

    def get_total_items(self):
        """Get the total number of items in the cart."""
        return sum(sum(x) for x in self.cart.values())

    def get_cart_details(self):
        """Get the details of all products in the cart."""
        return dict(self.cart)

# Define the views
@view_config(route_name='add_to_cart', renderer='json')
def add_to_cart(request):
    cart = request.session.get('cart', ShoppingCart())
    product_id = request.matchdict['product_id']
    quantity = int(request.matchdict.get('quantity', 1))
    try:
        cart.add_product(request, product_id, quantity)
    except ValueError as e:
        return {'error': str(e)}
    request.session['cart'] = dict(cart.cart)
    return {'message': 'Product added to cart successfully.', 'cart': dict(cart.cart)}

@view_config(route_name='remove_from_cart', renderer='json')
def remove_from_cart(request):
    cart = request.session.get('cart', ShoppingCart())
    product_id = request.matchdict['product_id']
    try:
        cart.remove_product(request, product_id)
    except KeyError as e:
        return {'error': str(e)}
    request.session['cart'] = dict(cart.cart)
    return {'message': 'Product removed from cart successfully.', 'cart': dict(cart.cart)}

@view_config(route_name='get_cart', renderer='json')
def get_cart(request):
    cart = request.session.get('cart', ShoppingCart())
    return {'total_items': cart.get_total_items(), 'cart_details': cart.get_cart_details()}

# Define the main function to set up the Pyramid application
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('add_to_cart', '/add_to_cart/{product_id}/{quantity}')
    config.add_route('remove_from_cart', '/remove_from_cart/{product_id}')
    config.add_route('get_cart', '/get_cart')
    config.scan()
    return config.make_wsgi_app()
