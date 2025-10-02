# 代码生成时间: 2025-10-03 02:11:27
# -*- coding: utf-8 -*-

"""
Crypto Wallet Application
=============================

This application demonstrates a simple implementation of a crypto wallet using the Pyramid framework.
It handles basic operations like creating a wallet, adding funds, and sending funds.

"""

import os
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.security import Allow, Authenticated, NO_PERMISSION_REQUIRED
from pyramid.authentication import AuthTktAuthenticationPolicy, CallbackAuthenticationPolicy
from pyramid.authorization import ACLAuthorizationPolicy
from pyramid.renderers import JSON
from pyramid.settings import aslist
from pyramid.exceptions import ConfigurationError
from pyramid.threadlocal import get_current_registry, get_current_request
from pyramid.httpexceptions import HTTPBadRequest

# Define a class for the wallet
class Wallet:
    def __init__(self, owner, initial_balance=0):
        self.owner = owner
        self.balance = initial_balance

    def add_funds(self, amount):
        """Add funds to the wallet"""
        if amount < 0:
            raise ValueError("Amount must be positive")
        self.balance += amount
        return self.balance

    def send_funds(self, recipient, amount):
        """Send funds to another wallet"""
        if amount < 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        # Assuming recipient is another wallet object
        recipient.add_funds(amount)
        self.balance -= amount
        return self.balance

# Create a dummy wallet for demonstration purposes
wallet = Wallet(owner="John Doe", initial_balance=1000)

# Define views
@view_config(route_name='home', renderer='json')
def home_view(request):
    return {"message": "Welcome to the crypto wallet application!"}

@view_config(route_name='get_balance', renderer='json')
def get_balance_view(request):
    return {"balance": wallet.balance}

@view_config(route_name='add_funds', request_method='POST', renderer='json')
def add_funds_view(request):
    try:
        amount = float(request.json.get("amount", 0))
        new_balance = wallet.add_funds(amount)
        return {"new_balance": new_balance}
    except ValueError as e:
        return {"error": str(e)}

@view_config(route_name='send_funds', request_method='POST', renderer='json')
def send_funds_view(request):
    try:
        recipient = request.json.get("recipient")
        amount = float(request.json.get("amount", 0))
        # For demonstration purposes, assume recipient is another wallet object
        if recipient == "wallet":
            new_balance = wallet.send_funds(wallet, amount)
        return {"new_balance": new_balance}
    except ValueError as e:
        return {"error": str(e)}

# Configure the Pyramid application
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include("pyramid_chameleon")
    # Define routes
    config.add_route('home', '/')
    config.add_route('get_balance', '/balance')
    config.add_route('add_funds', '/add_funds')
    config.add_route('send_funds', '/send_funds')
    # Define views
    config.scan()
    return config.make_wsgi_app()
