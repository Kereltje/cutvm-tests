

import os
import json


def open_doc(file_name: str, base_path: str = ''):
    fullpath = os.path.join(base_path, file_name)
    with open(fullpath, 'r') as f:
        return f.read()


def open_json(file_name: str, base_path: str = ''):
    data = open_doc(file_name, base_path)
    return json.loads(data)
