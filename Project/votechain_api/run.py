import os
import sys

# Obtiene el directorio actual del script
current_directory = os.path.dirname(__file__)

# Construye la ruta a votechain_api
votechain_api_path = os.path.join(current_directory, "votechain_api")

# Añade la ruta de votechain_api al sys.path
sys.path.append(votechain_api_path)


from stacks.auth import create_auth_app

auth_app = create_auth_app()

if __name__ == "__main__":
    auth_app.run(debug=True, port=5001)
