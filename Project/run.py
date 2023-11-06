import os
import sys
import logging

# Construye la ruta al directorio raíz del proyecto
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# ROOT_DIR = os.path.dirname(BASE_DIR)
PROJECT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))

# Añade la ruta del directorio raíz del proyecto al sys.path
sys.path.append(PROJECT_DIR)

# Crea las bases de datos
from layers.database.mysql.create_databases import create_databases, create_renaper_data

create_databases()
create_renaper_data(False) # Si es True, crea 300 registros falsos en la base de datos RENAPER

from votechain_api import create_app
from flask.logging import default_handler

LOG_LEVEL = os.getenv("LOG_LEVEL")
logger = logging.getLogger()
logger.addHandler(default_handler)

votechain_app = create_app()


@votechain_app.after_request
def set_security_headers(response):
    # Establece los encabezados de seguridad aquí
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers[
        "Strict-Transport-Security"
    ] = "max-age=86400; includeSubdomain; preload"
    response.headers[
        "Content-Security-Policy"
    ] = "default-src 'self'; img-src 'self'; script-src 'self'; style-src 'self'; object-src 'self'"
    response.headers["Http-Header"] = "value"

    return response


from apscheduler.schedulers.background import BackgroundScheduler
from Project.votechain_api.stacks.controller.functions.email.index import (
    clean_expired_verification_codes,
)
from layers.resources import IntegratorResources

resources = IntegratorResources()

sched = BackgroundScheduler(deamon=True)
sched.add_job(clean_expired_verification_codes, "interval", seconds=resources.params["SCHEDULE"]["INTERVAL"])
sched.start()

if __name__ == "__main__":
    votechain_app.run(debug=True, port=5001)
