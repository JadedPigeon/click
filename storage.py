import json

def save_to_file(path, data):
    with open(path, 'w') as f:
        json.dump(data, f)

def load_from_file(path):
    with open(path, 'r') as f:
        return json.load(f)
