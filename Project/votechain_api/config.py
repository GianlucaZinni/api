import os
from resources import IntegratorResources

class Config:
    
    # Access to the parameters resources
    resources = IntegratorResources()
    
    # Each Flask web application contains a secret key which used to sign session cookies for protection against cookie data tampering.
    SECRET_KEY = resources.params["SECRET_KEY"]
    SQLALCHEMY_DATABASE_URI = resources.params["DB_CONFIG"]["SQLALCHEMY"]["DATABASE_URI"]

    # Grabs the folder where the script runs.
    basedir = os.path.abspath(os.path.dirname(__file__))
    ROOT_DIR = os.path.dirname(basedir)  # INGSOFT-II

    # Enable debug mode, that will refresh the page when you make changes.
    DEBUG = True

    # Turn off the Flask-SQLAlchemy event system and warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False