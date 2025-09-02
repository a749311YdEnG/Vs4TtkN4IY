# 代码生成时间: 2025-09-03 05:36:50
# unzip_tool.py

"""
A simple Pyramid application that provides a tool to unzip files.
"""

from pyramid.config import Configurator
from pyramid.view import view_config
from pyramid.response import Response
from zipfile import ZipFile, ZIP_DEFLATED
import io
import os


# Define the root of the application
ROOT = os.path.dirname(os.path.abspath(__file__))


class UnzipTool:
    """
    A class to handle unzipping of files.
    """

    def __init__(self, request):
        self.request = request

    @view_config(route_name='unzip_file', renderer='json')
    def unzip_file(self):
        """
        View to handle the unzipping of files.
        """
        try:
            # Check if the file is provided in the request
            if 'file' not in self.request.POST:
                return {'error': 'No file provided.'}

            # Get the uploaded file
            file = self.request.POST['file'].file

            # Create a buffer to store the file contents
            buffer = io.BytesIO()
            buffer.write(file.read())
            buffer.seek(0)

            # Open the zip file
            with ZipFile(buffer, 'r') as zip_file:
                # Extract all the contents of the zip file to a temporary directory
                extract_path = os.path.join(ROOT, 'temp')
                zip_file.extractall(extract_path)

                # Return a success message with the path where the files were extracted
                return {'message': 'Files extracted successfully.', 'path': extract_path}
        except Exception as e:
            # Return an error message if an exception occurs
            return {'error': str(e)}


def main(global_config, **settings):
    """
    Pyramid application main function.
    """
    with Configurator(settings=settings) as config:
        # Add a route for the unzip file view
        config.add_route('unzip_file', '/unzip')
        # Scan for @view_config decorators
        config.scan()
        # Return the WSGI application
        return config.make_wsgi_app()
