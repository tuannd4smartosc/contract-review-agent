import os
import requests 

PLAYBOOK_FOLDER = "documents/contract_playbooks"

os.makedirs(PLAYBOOK_FOLDER, exist_ok=True)

def download_file(url: str, save_path: str):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status() 
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        print(f"Downloaded: {url} -> {save_path}")
    except Exception as e:
        print(f"Failed to download {url}: {e}")

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