from flask import Flask, session
from flask_oauthlib.client import OAuth
from database.mysql.index import MySQLHandler
from database.sqlalchemy.index import SQLAlchemyHandler
from resources import IntegratorResources


class AuthStack:
    def __init__(self, app: Flask = None):
        # Access to the parameters resources
        resources = IntegratorResources()

        # Flask OAUTH
        self.oauth = OAuth(app)
        
        # SQLAlchemy Handler
        self.sqlalchemy = SQLAlchemyHandler()
        self.db_session = self.sqlalchemy.connect("VOTECHAIN")

        # Google instance
        self.google = self.oauth.remote_app(
            "google",
            consumer_key=resources.params["GOOGLE_AUTH"]["client_id"],
            consumer_secret=resources.params["GOOGLE_AUTH"]["client_secret"],
            # Solicitar acceso al correo electrónico y al perfil del usuario
            request_token_params={
                "scope": "email profile",
            },
            base_url="https://www.googleapis.com/oauth2/v1/",
            request_token_url=None,
            access_token_method="POST",
            access_token_url="https://accounts.google.com/o/oauth2/token",
            authorize_url="https://accounts.google.com/o/oauth2/auth",
        )

        @self.google.tokengetter
        def get_google_oauth_token():
            return session.get("google_token")

# Create Votechain database connection
mysql_votechain = MySQLHandler("VOTECHAIN")

google_users = mysql_votechain.create_table(
    table_name="google_users",
    partition_key="google_id",
    sort_key="email",
    attributes=["verified_email", "name", "surname", "picture"],
)

votechain_users = mysql_votechain.create_table(
    table_name="votechain_users",
    partition_key="id",
    sort_key="email",
    attributes=[
        "name",
        "surname",
        "picture",
        "dni",
        "telefono",
    ],
)
