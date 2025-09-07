# 代码生成时间: 2025-09-07 16:52:09
# folder_organizer.py
"""
A Pyramid application that organizes files in a given directory.

This application will scan the specified directory, identify files based on
their extensions, and move them into corresponding subdirectories.
"""

import os
import shutil
from pyramid.config import Configurator
from pyramid.response import Response


class FolderOrganizer:
    """
    Organize files in a given directory into subdirectories based on file extensions.
    """
    def __init__(self, root_path):
        self.root_path = root_path

    def organize(self):
        """
        Organize files in the directory.
        """
        try:
            for item in os.listdir(self.root_path):
                item_path = os.path.join(self.root_path, item)
                if os.path.isfile(item_path):
                    extension = os.path.splitext(item)[1]
                    folder_path = os.path.join(self.root_path, extension[1:])
                    if not os.path.exists(folder_path):
                        os.makedirs(folder_path)
                    shutil.move(item_path, folder_path)
            return "Files organized successfully."
        except Exception as e:
            return f"An error occurred: {e}"

    def list_files(self):
        """
        List all files in the directory.
        """
        try:
            files = [f for f in os.listdir(self.root_path) if os.path.isfile(os.path.join(self.root_path, f))]
            return files
        except Exception as e:
            return f"An error occurred: {e}"


def main(global_config, **settings):
    """
    Create Pyramid application instance.
    """
    with Configurator(settings=settings) as config:
        # Add a route
        config.add_route('organize', '/organize')
        config.add_route('list_files', '/files')

        # Add a view callable for the 'organize' route
        config.add_view(organize_view, route_name='organize')

        # Add a view callable for the 'list_files' route
        config.add_view(list_files_view, route_name='list_files')

        # Scan the directory and organize files
        folder_organizer = FolderOrganizer(os.path.join(settings['here'], 'data'))
        folder_organizer.organize()

    return config.make_wsgi_app()


# Pyramid view functions
def organize_view(request):
    """
    View function to organize files in the directory.
    """
    folder_organizer = FolderOrganizer(os.path.join(request.registry.settings['here'], 'data'))
    result = folder_organizer.organize()
    return Response(result)


def list_files_view(request):
    """
    View function to list files in the directory.
    """
    folder_organizer = FolderOrganizer(os.path.join(request.registry.settings['here'], 'data'))
    files = folder_organizer.list_files()
    return Response(files)
