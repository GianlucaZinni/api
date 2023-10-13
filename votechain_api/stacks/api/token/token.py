import logging
from os import getenv
from common.common_logging import logging_handler
from handler.rest_request_handler import RequestHandler
from interfaces.clients_interfaces import ClientsInterface
from interfaces.tokens_interface import TokensInterface
from security.token_factory import TokenFactory, AcquireTokenException, UnauthorizedClientException

LOG_LEVEL = getenv("LOG_LEFEL")
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)
logger.info("Starting Token Functionalities..")

TENANT_ID = getenv("TENANT_ID_PARAMETER")
CLIENT_ID = getenv("CLIENT_ID_PARAMETER")

tokens_interface = TokensInterface(getenv("TOKENS_TABLE"), LOG_LEVEL)
clients_interface = ClientsInterface(getenv("CLIENT_TABLE"), LOG_LEVEL)
token_factory = TokenFactory(TENANT_ID, CLIENT_ID, clients_interface, tokens_interface)

@logging_handler(log_level=LOG_LEVEL)
def handler(event, context):
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
            token = token_factory.create(username, password, app_id)
        except(AcquireTokenException, UnauthorizedClientException) as e:
            self.logger.error(e.message)
            return self.response_bad_request(message="Invalid username, password or appId")
        
        return self.response_ok(
            {
                "access_token": token.access_token,
                "token_type": token.type,
                "expires_in": token.expires_in,
            }
        )