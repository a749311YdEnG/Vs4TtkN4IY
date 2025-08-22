# 代码生成时间: 2025-08-22 18:42:12
import os
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from zipfile import ZipFile
from io import BytesIO


# Define a function to decompress a zip file
def decompress_zip_file(zip_file_path, output_folder):
    try:
        # Create the output folder if it doesn't exist
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        with ZipFile(zip_file_path, 'r') as zip_ref:
            # Extract all files from the zip file to the output folder
            zip_ref.extractall(output_folder)
            return f"Files extracted to {output_folder}"
    except FileNotFoundError:
        return "File not found"
    except Exception as e:
        return f"An error occurred: {str(e)}"


# Pyramid route to handle decompression requests
@view_config(route_name='decompress', request_method='POST')
def decompress_view(request):
    # Retrieve the zip file from the request
    zip_file_stream = request.POST['zip_file'].file.stream
    zip_file_bytes = zip_file_stream.read()
    output_folder = 'decompressed_files'

    # Use BytesIO to create a file-like object from the bytes
    zip_file = BytesIO(zip_file_bytes)
    zip_file_path = 'temp.zip'
    zip_file.close()

    # Save the zip file to the server
    with open(zip_file_path, 'wb') as f:
        f.write(zip_file_bytes)

    # Decompress the zip file
    result = decompress_zip_file(zip_file_path, output_folder)

    # Remove the temporary zip file after decompression
    os.remove(zip_file_path)

    # Return the result of the decompression
    return Response(result, content_type='text/plain')


# Configure the Pyramid app
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
    config.add_route('decompress', '/decompress')
    config.scan()
    return config.make_wsgi_app()
