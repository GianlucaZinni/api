from flask import Flask, session
from flask_oauthlib.client import OAuth
import os
from layers.resources import IntegratorResources


class ApiStack:
    def __init__(self, app: Flask = None):
        # Access to the parameters resources
        resources = IntegratorResources()

        # Flask OAUTH
        self.oauth = OAuth(app)

        # SQLAlchemy Handler
        self.count_nro_tramite = 4
        self.message = ""
        self.message_email = ""

        # Google instance
        self.google_key = self.oauth.remote_app(
            "google",
            consumer_key=os.getenv("GOOGLE-CLIENT_ID"),
            consumer_secret=os.getenv("GOOGLE-CLIENT_SECRET"),
            request_token_params={
                "scope": "email profile",
            },
            base_url="https://www.googleapis.com/oauth2/v1/",
            request_token_url=None,
            access_token_method="POST",
            access_token_url="https://accounts.google.com/o/oauth2/token",
            authorize_url="https://accounts.google.com/o/oauth2/auth",
        )

        @self.google_key.tokengetter
        def get_google_oauth_token():
            return session.get("google_token")

api = ApiStack()