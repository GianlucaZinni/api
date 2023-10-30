from flask import Flask
from flask_cors import CORS
from votechain_api.config import Config
from votechain_api.stacks import Votechain


def create_app(config_class=Config):
    # Flask app object
    app = Flask(__name__)

    CORS(app)

    # Configuring from Python Files
    app.config.from_object(config_class)
    Votechain(app)

    from votechain_api.stacks.auth.functions.google_auth.index import google_auth
    from votechain_api.stacks.auth.functions.votechain_auth.index import votechain_auth
    from votechain_api.stacks.vote.functions.votacion.index import votacion

    app.register_blueprint(google_auth)
    app.register_blueprint(votechain_auth)
    app.register_blueprint(votacion)

    return app
