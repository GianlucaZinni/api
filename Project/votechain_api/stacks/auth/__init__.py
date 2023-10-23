from flask import Flask
from flask_cors import CORS
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy
from stacks.database.functions.mysql_handler import MySQLDatabaseHandler


class AuthStack:
    def __init__(self, app: Flask):
        self.app = app
        self.mysql = MySQLDatabaseHandler(database_name="Auth_db")
        
        # Configuración de Flask
        app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:42886236@localhost/auth_db"
        app.secret_key = "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"
        
        self.db = SQLAlchemy(app)
        self.oauth = OAuth(app)

        # Configuración de Google OAuth
        app.config[
            "GOOGLE_ID"
        ] = "763831980100-jla6gkspnss9vqkc13kblqe9mjht0ib1.apps.googleusercontent.com"
        app.config["GOOGLE_SECRET"] = "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"
        app.config["GOOGLE_REDIRECT_URI"] = "/google/login/authorized"

        self.google = self.oauth.remote_app(
            "google",
            consumer_key=app.config["GOOGLE_ID"],
            consumer_secret=app.config["GOOGLE_SECRET"],
            request_token_params={
                "scope": "email profile",  # Solicitar acceso al correo electrónico y al perfil del usuario
            },
            base_url="https://www.googleapis.com/oauth2/v1/",
            request_token_url=None,
            access_token_method="POST",
            access_token_url="https://accounts.google.com/o/oauth2/token",
            authorize_url="https://accounts.google.com/o/oauth2/auth",
        )

        # Configuración de tablas de base de datos
        self.google_users = self.mysql.create_table(
            table_name="google_users",
            partition_key="google_id",
            sort_key="email",
            attributes=["verified_email", "name", "surname", "picture"],
        )

        self.votechain_users = self.mysql.create_table(
            table_name="votechain_users",
            partition_key="id",
            sort_key="email",
            attributes=[
                "name",
                "surname",
                "picture",
                "dni",
                "telefono",
                "public_key",
                "private_key",
            ],
        )

app = Flask(__name__)
CORS(app)
auth_app = AuthStack(app)

from stacks.auth.functions.google_auth.index import google_auth
from stacks.auth.functions.votechain_auth.index import votechain_auth

# Pasa la instancia de auth_app al blueprint google_auth
google_auth.auth_app = auth_app

app.register_blueprint(google_auth)
app.register_blueprint(votechain_auth)


def create_auth_app():
    return app
