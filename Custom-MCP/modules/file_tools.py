import os

def list_files(path="."):
    try:
        return os.listdir(path)
    except Exception as e:
        return [str(e)]

def create_dir(folder_name):
    try:
        os.makedirs(folder_name, exist_ok=True)
        return f"Directory '{folder_name}' created."
    except Exception as e:
        return str(e)

def delete_file(file_path):
    try:
        os.remove(file_path)
        return f"File '{file_path}' deleted."
    except Exception as e:
        return str(e)
