from flask import Flask
from stacks.api.apps.auth.app import auth_app
from stacks.api.apps.restapi.app import restapi_app
from stacks.api.apps.token.app import token_app
app = Flask(__name__)

# Registrar las aplicaciones
app.register_blueprint(auth_app)
app.register_blueprint(restapi_app)
app.register_blueprint(token_app)

if __name__ == '__main__':
    app.run()
