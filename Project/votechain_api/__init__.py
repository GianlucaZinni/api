from flask import Flask
from flask_cors import CORS
from flask_session import Session
from votechain_api.config import Config
from votechain_api.stacks import Votechain
from dotenv import load_dotenv


def create_app(config_class=Config):
    load_dotenv()
    # Flask app object
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    CORS(app)
    Session(app)

    # Configuring from Python Files
    Votechain(app)

    from votechain_api.stacks.api.functions.google_auth.routes import google_auth
    from votechain_api.stacks.api.functions.vote_auth.routes import vote_auth
    from votechain_api.stacks.api.functions.vote.routes import vote

    app.register_blueprint(google_auth)
    app.register_blueprint(vote_auth)
    app.register_blueprint(vote)

    return app
