import json


def save_log(file_path: str, res: dict):
    with open(file_path, 'w') as f:
        f.write(json.dumps(res))
