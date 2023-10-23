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

# Configuración de encabezados de seguridad
app.config.update(
    SESSION_COOKIE_SECURE=True,  # Cookies solo se envían a través de conexiones seguras (HTTPS)
    SESSION_COOKIE_HTTPONLY=True,  # Cookies solo accesibles a través de HTTP y no JavaScript
    SESSION_COOKIE_SAMESITE="Lax",  # Cookies se envían en solicitudes de navegación principales
    # Establece un encabezado de seguridad adicional para prevenir ataques de Directory Traversal
    #                  APPLICATION_ROOT="/your-root",  # Reemplaza "your-root" por la ruta de tu aplicación
)


@app.after_request
def set_security_headers(
    response,
):  # https://flask.palletsprojects.com/en/3.0.x/security/
    # Establece el encabezado "X-Content-Type-Options" en "nosniff"
    # para evitar que el navegador interprete incorrectamente el tipo de contenido.
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Configura el encabezado "X-Frame-Options" en "DENY" para evitar la inserción de la aplicación en un marco (frame).
    response.headers["X-Frame-Options"] = ("DENY",)

    # Activa la protección XSS (Cross-Site Scripting) en el navegador con el valor "1; mode=block".
    response.headers["X-XSS-Protection"] = ("1; mode=block",)

    # Establece el encabezado "Strict-Transport-Security" (HSTS) para forzar la conexión a través de HTTPS
    # y prevenir ataques Man-in-the-Middle (MITM).
    response.headers["Strict-Transport-Security"] = (
        "max-age=86400; includeSubdomain; preload",
    )

    # Define una política de seguridad de contenido (CSP) que restringe las fuentes de recursos permitidas.
    response.headers[
        "Content-Security-Policy"
    ] = "default-src 'self'; img-src 'self'; script-src 'self'; style-src 'self'; object-src 'self'"

    response.headers["Http-Header"] = "value"

    return response


if __name__ == "__main__":
    app.run(debug=True)