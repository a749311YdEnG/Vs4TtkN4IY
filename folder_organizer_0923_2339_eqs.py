# 代码生成时间: 2025-09-23 23:39:37
# folder_organizer.py

"""
Folder Organizer is a Python script using Pyramid framework to organize
the structure of a given folder. It moves files into a categorized
structure based on the file extensions.
"""

from pathlib import Path
import os
import shutil
from typing import Dict

# Define a dictionary to map file extensions to folder names
EXTENSION_MAP: Dict[str, str] = {
    '.jpg': 'Images',
    '.jpeg': 'Images',
    '.png': 'Images',
    '.gif': 'Images',
    '.txt': 'Documents',
    '.pdf': 'Documents',
    '.docx': 'Documents',
    '.xlsx': 'Spreadsheets',
    '.csv': 'Spreadsheets',
    # Add more extensions and folder mappings as needed
}


def organize_folder(source_folder: Path) -> None:
    """Organize the files in the given source folder based on their extensions."""
    # Check if the source folder exists
    if not source_folder.is_dir():
        raise FileNotFoundError(f"The source folder {source_folder} does not exist.")

    # Create a new folder for each file type
    for extension, folder_name in EXTENSION_MAP.items():
        folder_path = source_folder / folder_name
        folder_path.mkdir(exist_ok=True)  # Create the folder if it does not exist

    # Move files into the corresponding folders
    for file_path in source_folder.iterdir():
        if file_path.is_file():
            file_extension = file_path.suffix.lower()
            if file_extension in EXTENSION_MAP:
                target_folder = source_folder / EXTENSION_MAP[file_extension]
                target_path = target_folder / file_path.name

                # Move the file to the new location
                try:
                    shutil.move(str(file_path), str(target_path))
                except Exception as e:
                    print(f"Error moving file {file_path} to {target_path}: {e}")


def main():
    # Specify the source folder path
    source_folder_path = Path('/path/to/source/folder')
    try:
        organize_folder(source_folder_path)
        print(f"Folder structure organized in {source_folder_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()