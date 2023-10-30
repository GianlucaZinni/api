import os
import sys

# Construye la ruta al directorio raíz del proyecto
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# ROOT_DIR = os.path.dirname(BASE_DIR)
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Añade la ruta del directorio raíz del proyecto al sys.path
sys.path.append(PROJECT_DIR)

from database.mysql.index import MySQLHandler

# Initializing raw database creation
MySQLHandler()

from votechain_api import create_app
votechain_app = create_app()

if __name__ == "__main__":
    votechain_app.run(debug=True, port=5001)
