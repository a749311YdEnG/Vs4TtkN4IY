# 代码生成时间: 2025-08-21 13:38:44
# hash_calculator.py

"""
A Pyramid application to calculate hash values for given input.
"""

from pyramid.config import Configurator
from pyramid.response import Response
import hashlib
import json


# Define the HashCalculator class to handle hash calculations
class HashCalculator:
    def __init__(self):
        # Initialize the hash calculation tool
        pass
    
    # Method to calculate hash values
    def calculate_hash(self, input_string, hash_type='sha256'):
        """
        Calculate the hash value for the given input string.
        
        :param input_string: The string to calculate the hash for.
        :param hash_type: The type of hash (e.g., 'sha256', 'md5', etc.).
        :return: A dictionary containing the hash type and the calculated hash value.
        """
        hash_types = {'sha256': hashlib.sha256, 'md5': hashlib.md5}
        try:
            hash_function = hash_types[hash_type]
        except KeyError:
            raise ValueError(f