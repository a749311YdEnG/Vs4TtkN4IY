# 代码生成时间: 2025-08-11 14:21:30
import os
import shutil

"""
A folder organizer application which helps to organize files into
specific directories based on their file extensions.
"""

class FolderOrganizer:
    def __init__(self, source_dir):
        """
        Initialize the FolderOrganizer with the source directory to organize.
        :param source_dir: The path to the directory to be organized.
        """
        self.source_dir = source_dir
        self.extensions = {
            '.txt': 'Text Files',
            '.docx': 'Word Documents',
            '.pdf': 'PDF Files',
            '.png': 'Image Files',
            '.jpg': 'Image Files',
            '.jpeg': 'Image Files',
            '.mp3': 'Audio Files',
            '.mp4': 'Video Files',
        }

    def organize(self):
        """
        Organize the files in the source directory into subdirectories
        based on their extensions.
        """
        for root, dirs, files in os.walk(self.source_dir):
            for file in files:
                file_path = os.path.join(root, file)
                extension = os.path.splitext(file)[1].lower()

                if extension in self.extensions:
                    target_dir = os.path.join(root, self.extensions[extension])
                    self._create_directory(target_dir)
                    self._move_file(file_path, target_dir)

    def _create_directory(self, directory):
        """
        Create a directory if it does not exist.
        :param directory: The path to the directory to be created.
        """
        try:
            os.makedirs(directory, exist_ok=True)
        except OSError as e:
            print(f"Error creating directory {directory}: {e}")

    def _move_file(self, file_path, target_dir):
        """
        Move a file to a target directory.
        :param file_path: The path to the file to be moved.
        :param target_dir: The path to the target directory.
        """
        try:
            shutil.move(file_path, target_dir)
        except OSError as e:
            print(f"Error moving file {file_path} to {target_dir}: {e}")

    def __del__(self):
        """
        Destructor to clean up any resources if necessary.
        """
        pass

# Example usage
if __name__ == '__main__':
    source_directory = '/path/to/your/source/directory'
    organizer = FolderOrganizer(source_directory)
    organizer.organize()
    print('Folder organization completed.')