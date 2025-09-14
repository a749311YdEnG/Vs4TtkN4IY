# 代码生成时间: 2025-09-15 04:26:32
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.response import Response
from pyramid.security import Authenticated
from pyramid.httpexceptions import HTTPFound
from pyramid.request import Request
from pyramid.threadlocal import get_current_registry
from pyramid.threadlocal import get_current_request

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError


# Define the database models
from models import DBSession, CartItem, Product

# Define the shopping cart service
class ShoppingCartService:
    def __init__(self, request):
        self.request = request

    def add_to_cart(self, product_id):
        try:
            # Get the current user from the request
            current_user = self.request.authenticated_userid

            # Get the product and the cart item
            product = DBSession.query(Product).get(product_id)
            if not product:
                return False

            # Check if the item is already in the cart
            cart_item = DBSession.query(CartItem).filter(
                CartItem.user_id == current_user,
                CartItem.product_id == product_id).first()
            if cart_item:
                # Increment the quantity
                cart_item.quantity += 1
            else:
                # Create a new cart item
                cart_item = CartItem(user_id=current_user, product_id=product_id, quantity=1)
                DBSession.add(cart_item)

            # Commit changes
            DBSession.commit()
            return True
        except SQLAlchemyError as e:
            DBSession.rollback()
            return False

    def remove_from_cart(self, cart_item_id):
        try:
            cart_item = DBSession.query(CartItem).get(cart_item_id)
            if not cart_item:
                return False

            # Remove the cart item
            DBSession.delete(cart_item)
            DBSession.commit()
            return True
        except SQLAlchemyError as e:
            DBSession.rollback()
            return False


# Pyramid views
@view_config(route_name='add_to_cart', request_method='POST', permission=Authenticated)
def add_to_cart(request):
    product_id = request.params.get('product_id')
    if product_id:
        cart_service = ShoppingCartService(request)
        if cart_service.add_to_cart(product_id):
            return HTTPFound(location=request.route_url('view_cart'))
    return Response('Error adding product to cart', status=500)

@view_config(route_name='remove_from_cart', request_method='POST', permission=Authenticated)
def remove_from_cart(request):
    cart_item_id = request.params.get('cart_item_id')
    if cart_item_id:
        cart_service = ShoppingCartService(request)
        if cart_service.remove_from_cart(cart_item_id):
            return HTTPFound(location=request.route_url('view_cart'))
    return Response('Error removing product from cart', status=500)


# Pyramid configuration
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    engine = create_engine('your_database_engine_here')
    DBSession.configure(bind=engine)

    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('view_cart', '/cart')
    config.add_route('add_to_cart', '/add_to_cart')
    config.add_route('remove_from_cart', '/remove_from_cart')
    config.scan()
    return config.make_wsgi_app()


if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    from pyramid.paster import get_app
    app = get_app('development.ini', 'main')
    server = make_server('0.0.0.0', 6543, app)
    server.serve_forever()