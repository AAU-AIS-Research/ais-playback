import os
from tests.constants import TEMP_DATA_FOLDER


def clear_temp_folder():
    """Clear the temp folder."""
    if os.path.basename(TEMP_DATA_FOLDER) == 'temp':
        for folder in os.listdir(TEMP_DATA_FOLDER):
            path = os.path.join(TEMP_DATA_FOLDER, folder)
            if os.path.isdir(path):
                for file in os.listdir(path):
                    file_path = os.path.join(path, file)
                    os.remove(file_path)
                os.rmdir(path)
            else:
                os.remove(path)


def number_of_files_in_folder(folder_path: str) -> int:
    """Return the number of files in a folder."""
    return len([name for name in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, name))])


def number_of_folders_in_folder(folder_path: str) -> int:
    """Return the number of folders in a folder."""
    return len([name for name in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, name))])


def file_exists(file_path: str) -> bool:
    """Return True if the file exists."""
    return os.path.isfile(file_path)
