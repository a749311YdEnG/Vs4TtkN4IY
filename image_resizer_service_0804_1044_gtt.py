# 代码生成时间: 2025-08-04 10:44:57
# -*- coding: utf-8 -*-

"""
Image Resizer Service
====================

A Pyramid application for resizing images in batch.

Usage:
    python setup.py develop
    ./bin/image_resizer_service --port=8080
# TODO: 优化性能
"""

import os
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
from pyramid.renderers import render_to_response
from pyramid.renderers import JSON
from PIL import Image
from io import BytesIO
# 改进用户体验

# Define the default configuration for the image resizer
DEFAULT_RESIZE_WIDTH = 800
DEFAULT_RESIZE_HEIGHT = 600
DEFAULT_IMAGE_FORMAT = 'JPEG'

class ImageResizerService:
    """
# 添加错误处理
    Service class responsible for resizing images.
# 扩展功能模块
    """
    def __init__(self, config):
        self.config = config

    @view_config(route_name='resize_images', renderer='json')
    def resize_images(self):
        """
        Resize multiple images and return a list of new image URLs.
        """
        new_image_urls = []
        try:
            image_paths = self.request.params.getall('image_paths')
            width = int(self.request.params.get('width', DEFAULT_RESIZE_WIDTH))
            height = int(self.request.params.get('height', DEFAULT_RESIZE_HEIGHT))

            # Resize each image and add the new image URL to the list
            for image_path in image_paths:
# NOTE: 重要实现细节
                new_image_url = self.resize_image(image_path, width, height)
                new_image_urls.append(new_image_url)

        except Exception as e:
            return {"error": str(e)}

        return {"new_image_urls": new_image_urls}

    def resize_image(self, image_path, width, height):
        """
        Resize a single image and return the new image URL.
        """
        try:
            # Open the image file
            with Image.open(image_path) as img:
                # Resize the image and convert it to a BytesIO object
                img = img.resize((width, height), Image.ANTIALIAS)
# NOTE: 重要实现细节
                output = BytesIO()
                img.save(output, format=DEFAULT_IMAGE_FORMAT)
# 扩展功能模块
                output.seek(0)

                # Save the resized image to a temporary file and return its URL
                temp_file = self.save_temp_file(output)
# 添加错误处理
                return os.path.basename(temp_file)

        except Exception as e:
            raise ValueError(f"Failed to resize image {image_path}: {str(e)}")

    def save_temp_file(self, image_data):
        """
# 扩展功能模块
        Save the image data to a temporary file and return its path.
        """
        import tempfile
# TODO: 优化性能
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        temp_file.write(image_data.read())
        temp_file.close()
        return temp_file.name

# Configure the Pyramid application
# NOTE: 重要实现细节
def main(global_config, **settings):
    with Configurator(settings=settings) as config:
        config.include('pyramid_chameleon')
# 增强安全性
        config.include('pyramid_jinja2')
# 改进用户体验

        # Add the ImageResizerService to the config registry
# 添加错误处理
        config.registry['image_resizer_service'] = ImageResizerService(config)
# 改进用户体验

        # Define the routes and views
# 增强安全性
        config.add_route('resize_images', '/resize')
        config.scan()

    return config.make_wsgi_app()
# NOTE: 重要实现细节
