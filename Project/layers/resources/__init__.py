import re
from json import load, loads
from os.path import isfile
from os import getenv
import os
from dotenv import load_dotenv

# Carga las variables de entorno desde el archivo .env
load_dotenv()
root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
print(root)

class IntegratorResources:
    
    def __init__(self, file_path: str = None):
        
        self.params = get_env_params(file_path=file_path)
        
    @staticmethod
    def normalize_name(name: str) -> str:
        name = re.sub("(.*)/", "", name)
        name = name.replace("-", "_")
        return re.sub("?<!^)(?=[A-Z])", "_", name).lower()
    
def get_env_params(*, env: str = getenv("PARAMS"), file_path: str = None) -> dict:
    json_file_path = file_path if file_path else f"{root}\params\{env}.json"
    if file_path and not isfile(file_path):
        raise ValueError(f"{file_path} not exists")
    if not isfile(json_file_path):
        raise ValueError(f"{json_file_path} not exists")
    params = load(open(json_file_path, encoding="utf-8"))
    return {**params}