import os

def create_file_exist(file_path: str) -> bool:
    return os.path.exists(file_path)