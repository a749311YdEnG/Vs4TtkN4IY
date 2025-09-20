# 代码生成时间: 2025-09-20 17:45:21
# data_analysis_service.py

"""
A simple data analysis service using the Pyramid framework.
This service provides basic data analysis functionalities such as mean, median, and standard deviation.
"""

from pyramid.view import view_config
from pyramid.response import Response
import numpy as np


# Define the DataAnalysisService class
class DataAnalysisService:
    """Service class to perform data analysis."""

    def calculate_mean(self, data):
        """Calculate the mean of a given data set."""
        try:
            return np.mean(data)
        except TypeError:
            return 'Error: Data provided is not numeric.'
        except Exception as e:
            return f'An error occurred: {e}'

    def calculate_median(self, data):
        """Calculate the median of a given data set."""
        try:
            return np.median(data)
        except TypeError:
            return 'Error: Data provided is not numeric.'
        except Exception as e:
            return f'An error occurred: {e}'

    def calculate_std_deviation(self, data):
        """Calculate the standard deviation of a given data set."""
        try:
            return np.std(data)
        except TypeError:
            return 'Error: Data provided is not numeric.'
        except Exception as e:
            return f'An error occurred: {e}'

# Define the Pyramid view for the data analysis service
@view_config(route_name='calculate_mean', request_method='POST', renderer='json')
def calculate_mean_view(request):
    """View function to calculate and return the mean of the data."""
    service = DataAnalysisService()
    data = request.json.get('data', [])
    result = service.calculate_mean(data)
    return {'mean': result}

@view_config(route_name='calculate_median', request_method='POST', renderer='json')
def calculate_median_view(request):
    """View function to calculate and return the median of the data."""
    service = DataAnalysisService()
    data = request.json.get('data', [])
    result = service.calculate_median(data)
    return {'median': result}

@view_config(route_name='calculate_std_deviation', request_method='POST', renderer='json')
def calculate_std_deviation_view(request):
    """View function to calculate and return the standard deviation of the data."""
    service = DataAnalysisService()
    data = request.json.get('data', [])
    result = service.calculate_std_deviation(data)
    return {'std_deviation': result}
