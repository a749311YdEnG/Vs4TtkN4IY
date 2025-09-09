# 代码生成时间: 2025-09-09 19:53:06
from pyramid.config import Configurator
from pyramid.view import view_config, view_defaults
from pyramid.renderers import JSON
from pyramid.response import Response
from pyramid.httpexceptions import HTTPNotFound, HTTPInternalServerError

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define your database model
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# Create a database connection and session
engine = create_engine('sqlite:///users.db')
Session = sessionmaker(bind=engine)
Base.metadata.create_all(engine)

# Define your view functions
@view_defaults(renderer=JSON)
class UserAPI:
    def __init__(self, request):
        self.request = request
        self.session = Session()

    @view_config(route_name='users', request_method='GET')
    def get_users(self):
        """
        Get all users
        """
        try:
            users = self.session.query(User).all()
            return users
        except Exception as e:
            return HTTPInternalServerError('An error occurred while getting users.')

    @view_config(route_name='users', request_method='POST')
    def add_user(self):
        """
        Add a new user
        """
        data = self.request.json_body
        try:
            user = User(name=data['name'], email=data['email'])
            self.session.add(user)
            self.session.commit()
            return user, 201
        except Exception as e:
            self.session.rollback()
            return HTTPInternalServerError('An error occurred while adding user.')

    @view_config(route_name='users/{id}', request_method='GET')
    def get_user(self, id):
        """
        Get a single user by id
        """
        try:
            user = self.session.query(User).get(id)
            if user:
                return user
            else:
                return HTTPNotFound('User not found.')
        except Exception as e:
            return HTTPInternalServerError('An error occurred while getting a user.')

# Configure the Pyramid app
def main(global_config, **settings):
    """
    This function returns a Pyramid WSGI application.
    """
    config = Configurator(settings=settings)

    # Set up the routes
    config.add_route('users', '/users')
    config.add_route('user', '/users/{id}')

    # Scan for @view_config decorated functions and register them
    config.scan()

    return config.make_wsgi_app()
