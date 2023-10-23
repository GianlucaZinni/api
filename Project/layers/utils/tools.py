import json

def load_credentials(credentials_file):
    with open(credentials_file, "r") as file:
        return json.load(file)
