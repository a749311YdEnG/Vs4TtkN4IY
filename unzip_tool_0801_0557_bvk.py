# 代码生成时间: 2025-08-01 05:57:45
# unzip_tool.py - A Pyramid-based application for file extraction

from pyramid.config import Configurator
from pyramid.renderers import render_to_response
from pyramid.response import FileResponse
from pyramid.view import view_config
from zipfile import ZipFile
import os
import io

# Define a function to extract files from a given zip file
# 添加错误处理
def extract_zip(zip_path, extract_to):
# 优化算法效率
    with ZipFile(zip_path, 'r') as zip_file:
        # Extract all files from the zip file
        zip_file.extractall(extract_to)

# Pyramid view that handles file extraction
@view_config(route_name='extract', request_method='POST')
def extract_file(request):
    # Get uploaded zip file from request
    zip_file = request.POST['zip_file'].file
# 改进用户体验
    file_name = zip_file.filename

    # Check if the uploaded file is a zip file
    if not file_name.endswith('.zip'):
        return render_to_response('error.jinja2', {'error': 'Unsupported file type'}, request)

    # Create a temporary directory to extract files
# FIXME: 处理边界情况
    temp_dir = 'temp/'
    os.makedirs(temp_dir, exist_ok=True)

    try:
        # Extract the zip file to the temporary directory
        extract_zip(io.BytesIO(zip_file.read()), temp_dir)

        # List extracted files and return their names
        extracted_files = os.listdir(temp_dir)
        return render_to_response('success.jinja2', {'files': extracted_files}, request)

    except Exception as e:
        # Handle any errors during extraction and return an error message
        return render_to_response('error.jinja2', {'error': str(e)}, request)
    finally:
        # Clean up the temporary directory after extraction
        import shutil
        shutil.rmtree(temp_dir)

# Pyramid main function to set up the application
def main(global_config, **settings):
    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')
# 添加错误处理
    config.add_route('extract', '/extract')
    config.scan()
    return config.make_wsgi_app()
