import logging
from os import getenv

from layers.common.common_logging import logging_handler
from layers.interfaces.clients_permissions_interface import ClientsPermissionsInterface
from layers.interfaces.resources_permissions_interface import ResourcesPermissionsInterface
from layers.interfaces.tokens_interface import TokensInterface
from layers.security.auth_policy import AuthPolicy
from layers.security.authorization_handler import AuthorizationHandler, MissingTokenException
from flask import Blueprint

# Configuración de nivel de registro
LOG_LEVEL = getenv("LOG_LEVEL")
logger = logging.getLogger()
logger.setLevel(LOG_LEVEL)
logger.info("Starting lambda container")

auth_app = Blueprint('auth', __name__)

# Instancias de interfaces y manejadores
tokens_interface = TokensInterface(getenv("TOKENS_TABLE"), LOG_LEVEL)
clients_permissions_interface = ClientsPermissionsInterface(getenv("CLIENTS_PERMISSIONS_TABLE"), LOG_LEVEL)
resources_permissions_interface = ResourcesPermissionsInterface(getenv("RESOURCES_PERMISSIONS_TABLE"), LOG_LEVEL)

authorization_handler = AuthorizationHandler(
    tokens_interface, clients_permissions_interface, resources_permissions_interface
)

def get_header_value(event: dict, key: str, default: str = None):
    return event["headers"].get(key, event["headers"].get(key.lower(), default))

def get_access_token(event):
    auth_header = get_header_value(event, "Authorization", "")
    auth_header_parts = auth_header.split(" ")

    if len(auth_header_parts) == 2 and auth_header_parts[0].upper() == "BEARER":
        return auth_header_parts[1]

    return ""

@logging_handler(log_level=LOG_LEVEL)
def handler(event, unused_context):
    logger.debug(event)
    
    method_arn = event["methodArn"].split(":")
    region = method_arn[3]
    aws_account_id = method_arn[4]
    api_gateway_arn_tmp = method_arn[5].split("/")
    rest_api_id = api_gateway_arn_tmp[0]
    stage = api_gateway_arn_tmp[1]
    resource = event["resource"]
    http_method = event["httpMethod"]

    policy = AuthPolicy("user", aws_account_id, region, stage, rest_api_id)

    access_token = get_access_token(event)
    app_id = get_header_value(event, "appId")
    client_info = None

    try:
        client_info = authorization_handler.get_client_info(access_token, app_id)
    except MissingTokenException as e:
        logger.info(e.message)
        # Aquí se debería retornar un 401, pero AWS solo lo permite con raise Exception("Unauthorized") lo cual genera errores en las métricas de logs
        # Esto con nodejs se puede, refactorizar cuando se implemente para python

    if client_info and authorization_handler.has_permission(client_info, http_method, resource):
        logger.info(f"Authorized to {http_method} {resource}. appId: {client_info.app_id} ({client_info.username})")
        policy.allow_all_methods()
        auth_response = policy.build()
        auth_response["context"] = {"appId": client_info.app_id, "username": client_info.username}
        return auth_response

    logger.info(f"Unauthorized to {http_method} {resource}. appId: {app_id}")

    policy.deny_all_methods()
    return policy.build()
