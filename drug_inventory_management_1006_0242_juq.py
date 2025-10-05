# 代码生成时间: 2025-10-06 02:42:27
from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from pyramid.renderers import render_to_response

from collections import OrderedDict

# Define a simple in-memory database for demonstration purposes
DRUG_INVENTORY = OrderedDict({
    'Aspirin': {'quantity': 100, 'price': 5.99},
    'Paracetamol': {'quantity': 150, 'price': 2.99},
    'Ibuprofen': {'quantity': 120, 'price': 3.99}
})


# Helper function to add a new drug to the inventory
def add_drug(drug_name, quantity, price):
    if drug_name in DRUG_INVENTORY:
        raise ValueError(f"Drug '{drug_name}' already exists in the inventory.")
    DRUG_INVENTORY[drug_name] = {'quantity': quantity, 'price': price}

# Helper function to update the quantity of a drug in the inventory
def update_quantity(drug_name, quantity):
    if drug_name not in DRUG_INVENTORY:
        raise ValueError(f"Drug '{drug_name}' does not exist in the inventory.")
    DRUG_INVENTORY[drug_name]['quantity'] = quantity

# Helper function to remove a drug from the inventory
def remove_drug(drug_name):
    if drug_name not in DRUG_INVENTORY:
        raise ValueError(f"Drug '{drug_name}' does not exist in the inventory.")
    del DRUG_INVENTORY[drug_name]

# View function to display the inventory
@view_config(route_name='inventory', renderer='json')
def inventory_view(request):
    return DRUG_INVENTORY

# View function to add a drug to the inventory
@view_config(route_name='add_drug', renderer='json')
def add_drug_view(request):
    try:
        drug_name = request.matchdict['drug_name']
        quantity = int(request.matchdict['quantity'])
        price = float(request.matchdict['price'])
        add_drug(drug_name, quantity, price)
        return {'status': 'success', 'message': 'Drug added successfully.'}
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}
    except (TypeError, ValueError):
        return {'status': 'error', 'message': 'Invalid input values.'}

# View function to update the quantity of a drug in the inventory
@view_config(route_name='update_quantity', renderer='json')
def update_quantity_view(request):
    try:
        drug_name = request.matchdict['drug_name']
        quantity = int(request.matchdict['quantity'])
        update_quantity(drug_name, quantity)
        return {'status': 'success', 'message': 'Drug quantity updated successfully.'}
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}
    except (TypeError, ValueError):
        return {'status': 'error', 'message': 'Invalid input values.'}

# View function to remove a drug from the inventory
@view_config(route_name='remove_drug', renderer='json')
def remove_drug_view(request):
    try:
        drug_name = request.matchdict['drug_name']
        remove_drug(drug_name)
        return {'status': 'success', 'message': 'Drug removed successfully.'}
    except ValueError as e:
        return {'status': 'error', 'message': str(e)}

# Configure the Pyramid application
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('inventory', '/inventory')
    config.add_route('add_drug', '/add_drug/{drug_name}/{quantity}/{price}')
    config.add_route('update_quantity', '/update_quantity/{drug_name}/{quantity}')
    config.add_route('remove_drug', '/remove_drug/{drug_name}')
    config.scan()
    return config.make_wsgi_app()
