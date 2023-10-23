import logging
from os import getenv
from votechain_layers.common.common_logging import logging_handler
from votechain_layers.web_services.request_handler import RequestHandler
from votechain_layers.interfaces.clients_interface import ClientsInterface
from votechain_layers.interfaces.tokens_interface import TokensInterface
from votechain_layers.database.parameterstore_handler import get_parameter_value
from votechain_layers.security.token_factory import TokenFactory, AcquireTokenException, UnauthorizedClientException
from flask import Flask
1
token_app = Flask(__name__)

LOG_LEVEL = getenv("LOG_LEVEL")
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)
logger.info("Starting lambda container")

class Token:
    def __init__(self):

        CLIENT_ID = get_parameter_value("CLIENT_ID_PARAMETER")
        CLIENT_SECRET = get_parameter_value("CLIENT_SECRET_PARAMETER")

        self.tokens_interface = TokensInterface(get_parameter_value("TOKENS_TABLE"), LOG_LEVEL)
        self.clients_interface = ClientsInterface(get_parameter_value("CLIENT_TABLE"), LOG_LEVEL)
        self.token_factory = TokenFactory(CLIENT_ID, CLIENT_SECRET, self.clients_interface, self.tokens_interface)

    @logging_handler(log_level=LOG_LEVEL)
    @token_app.route('/auth/token', methods=['POST'])
    def handler(self, event, context):
        request_handler = TokenRequestHandler(event)
        
        if request_handler.is_resource("/auth/token"):
            if request_handler.is_post():
                return request_handler.get_token()
        
        return request_handler.get_bad_request()

class TokenRequestHandler(RequestHandler):
    def __init__(self, event):
        super().__init__(event, logger, False)
        self.logger = logger
    
    def get_token(self):
        username = self.body.get("username").lower()
        password = self.body.get("password")
        app_id = self.body.get("app_id")
        
        try:
            token = self.token_factory.create(username, password, app_id)
        except(AcquireTokenException, UnauthorizedClientException) as e:
            self.logger.error(e.message)
            return self.response_bad_request(message="Invalid username, password, or appId")
        
        return self.response_ok(
            {
                "access_token": token.access_token,
                "token_type": token.type,
                "expires_in": token.expires_in,
            }
        )


if __name__ == '__main__':
    token_app.run(port=5003)