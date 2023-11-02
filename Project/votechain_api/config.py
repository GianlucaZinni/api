import os
from os import getenv


class Config:
    # Each Flask web application contains a secret key which used to sign session cookies for protection against cookie data tampering.
    SECRET_KEY = getenv("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = getenv("DATABASE_URI")

    # Grabs the folder where the script runs.
    basedir = os.path.abspath(os.path.dirname(__file__))

    # Enable debug mode, that will refresh the page when you make changes.
    DEBUG = True

    # Turn off the Flask-SQLAlchemy event system and warning
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Cookies solo se envían a través de conexiones seguras (HTTPS)
    SESSION_COOKIE_SECURE = True
    # Cookies solo accesibles a través de HTTP y no JavaScript
    SESSION_COOKIE_HTTPONLY = True
    # Cookies se envían en solicitudes de navegación principales
    SESSION_COOKIE_SAMESITE = "Lax" 
    
    SESSION_TYPE = "filesystem"