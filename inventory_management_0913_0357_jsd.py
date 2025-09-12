# 代码生成时间: 2025-09-13 03:57:08
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response
from pyramid.security import Deny, Allow
from pyramid.authentication import CallbackAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.session import SignedCookieSessionFactory
from pyramid_tm import transactional
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from zope.interface import Interface, implementer
from pyramid.interfaces import IAuthenticationPolicy, IAuthorizationPolicy


# Define the database URI
DATABASE_URI = 'sqlite:///inventory.db'

# Create the engine and the session factory
engine = create_engine(DATABASE_URI)
SessionFactory = sessionmaker(bind=engine)

# Define the base class for declarative models
Base = declarative_base(engine)

# Define the InventoryItem model
class InventoryItem(Base):
    __tablename__ = 'inventory_items'
    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    quantity = Column(Integer)
    price = Column(Float)

    # String representation of an InventoryItem
    def __str__(self):
        return f"InventoryItem(id={self.id}, name='{self.name}', quantity={self.quantity}, price={self.price})"

# Pyramid views
@view_config(route_name='home', renderer='json')
def home_view(request):
    """The home view, which displays a list of all inventory items."""
    with SessionFactory() as session:
        items = session.query(InventoryItem).all()
        return {'inventory_items': [str(item) for item in items]}

@view_config(route_name='add_item', renderer='json')
def add_item_view(request):
    """The view to add a new inventory item."""
    with SessionFactory() as session:
        try:
            name = request.json.get('name')
            quantity = request.json.get('quantity')
            price = request.json.get('price')
            if not all([name, quantity, price]):
                raise ValueError('Missing required fields')
            
            item = InventoryItem(name=name, quantity=quantity, price=price)
            session.add(item)
            session.commit()
            return {'message': 'Item added successfully', 'item': str(item)}
        except Exception as e:
            session.rollback()
            return {'error': str(e)}

@view_config(route_name='update_item', renderer='json')
def update_item_view(request):
    """The view to update an existing inventory item."""
    with SessionFactory() as session:
        try:
            item_id = request.json.get('id')
            name = request.json.get('name')
            quantity = request.json.get('quantity')
            price = request.json.get('price')
            item = session.query(InventoryItem).filter_by(id=item_id).first()
            if not item:
                raise ValueError('Item not found')
            if name:
                item.name = name
            if quantity:
                item.quantity = quantity
            if price:
                item.price = price
            session.commit()
            return {'message': 'Item updated successfully', 'item': str(item)}
        except Exception as e:
            session.rollback()
            return {'error': str(e)}


# Set up the Pyramid configuration
def main(global_config, **settings):
    """Main function to set up the Pyramid application."""
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.include('pyramid_tm')
    config.add_route('home', '/')
    config.add_route('add_item', '/add_item')
    config.add_route('update_item', '/update_item/*item_id')
    config.scan()
    return config.make_wsgi_app()


# Define authentication and authorization policies
class RootFactory(object):
    def __init__(self, request):
        self.request = request

    # ACLs for the root factory
    def __acl__(self):
        return [(Allow, 'view', 'home'), (Allow, 'edit', 'add_item'), (Allow, 'edit', 'update_item')]

    # Authentication policy
    def check_permission(self, permission, context, request):
        return permission in self.__acl__()[0][1:]

    # Authorization policy
    def permissions(self, context, request):
        return self.__acl__()


# Implement the authentication and authorization policies
@implementer(IAuthenticationPolicy)
class SimpleAuthPolicy(CallbackAuthenticationPolicy):
    def __init__(self, callback):
        self.__callback = callback

    def authenticated_userid(self, request):
        return self.__callback(request)

    def unauthenticated_userid(self, request):
        return None

@implementer(IAuthorizationPolicy)
class SimpleAuthzPolicy(ACLAuthorizationPolicy):
    def permits(self, context, principals, permission):
        if permission == 'view':
            return principals.contains('view')
        elif permission == 'edit':
            return principals.contains('edit')
        else:
            return Deny


# Set up the authentication callback
def check_apikey(request):
    api_key = 'your_api_key_here'
    return request.headers.get('X-API-KEY') == api_key


# Set up the Pyramid application with authentication and authorization
def main_with_auth(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.include('pyramid_tm')
    config.set_authentication_policy(SimpleAuthPolicy(check_apikey))
    config.set_authorization_policy(SimpleAuthzPolicy())
    config.add_route('home', '/')
    config.add_route('add_item', '/add_item')
    config.add_route('update_item', '/update_item/*item_id')
    config.scan()
    return config.make_wsgi_app()
