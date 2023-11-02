from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_bcrypt import Bcrypt
# from stacks.api import ApiStack
from stacks.client import ClientStack
from stacks.database.functions.mysql_handler import MySQLDatabaseHandler
# from .config import DEBUG, config_by_name
import requests

app = Flask(__name__)
CORS(app)
# app.config['DEBUG'] = DEBUG
mysqldb = MySQLDatabaseHandler()
client_stack = ClientStack(app)
csrf = CSRFProtect(app)
flask_bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    # app.config.from_object(config_by_name[config_name])
    flask_bcrypt.init_app(app)

    return app


# Ruta para autenticar y autorizar el acceso a la API
@app.route("/api-gateway/<path:path>", methods=["GET", "POST"])
@csrf.exempt
def api_gateway(path):
    # Verificar el token de autenticación (simplificado para el ejemplo)
    authorization_header = request.headers.get('Authorization')
    if not authorization_header or not authorization_header.startswith('Bearer '):
        return jsonify({'error': 'Unauthorized'}), 401

    # Redirigir la solicitud al microservicio correspondiente
    microservice_url = f"http://localhost:5001/{path}"  # Ejemplo de microservicio Auth
    response = (
        requests.get(microservice_url, json=request.json)
        if request.method == "POST"
        else requests.get(microservice_url)
    )

    return response.text, response.status_code

if __name__ == "__main__":
    app.run(debug=True)