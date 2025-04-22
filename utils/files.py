import os

def list_file_paths(folder_path):
    file_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths

def get_file_extension(file_path):
    _, extension = os.path.splitext(file_path)
    return extension.lower()

def check_extension(file_path, expected_extension):
    actual_extension = get_file_extension(file_path)
    return actual_extension == expected_extension.lower()

def get_all_file_paths_recursive(folder_path):
    file_paths = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_paths.append(file_path)
    return file_paths