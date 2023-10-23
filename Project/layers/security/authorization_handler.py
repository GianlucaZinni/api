from dataclasses import dataclass
from datetime import datetime
from common.common_logging import init_logger
from interfaces.clients_permissions_interface import ClientsPermissionsInterface
from interfaces.resources_permissions_interface import ResourcesPermissionsInterface
from interfaces.tokens_interface import TokensInterface


class MissingTokenException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


@dataclass
class ClientInfo:
    username: str
    access_token_aad: int
    app_id: str
    permissions: set


class AuthorizationHandler:
    def __init__(
        self,
        tokens_interface: TokensInterface,
        clients_permissions_interface: ClientsPermissionsInterface,
        resources_permissions_interface: ResourcesPermissionsInterface,
        log_level=None,
    ):
        self.tokens_interface = tokens_interface
        self.clients_permissions_interface = clients_permissions_interface
        self.resources_permissions_interface = resources_permissions_interface
        self.logger = init_logger(__name__, log_level)

    def get_client_info(self, access_token: str, app_id: str) -> ClientInfo:
        token = self.tokens_interface.get_item(access_token, app_id) if access_token and app_id else None

        if not token or token["expires"] < int(datetime.now().timestamp()):
            raise MissingTokenException(f"El token no existe o caducó. appId: {app_id}")

        client_permissions_items = self.clients_permissions_interface.get_all_for_client(app_id)

        return ClientInfo(
            username=token["username"],
            access_token_aad=token["access_token_aad"],
            app_id=token["app_id"],
            permissions={item["permission"] for item in client_permissions_items},
        )

    def has_permission(self, client: ClientInfo, method: str, resource: str) -> bool:
        resource_permissions_items = self.resources_permissions_interface.get_all_for_resource(method, resource)

        resource_permissions = [item["permission"] for item in resource_permissions_items]

        self.logger.debug(f"resource_permissions: {resource_permissions}. client_permissions: {client.permissions}")

        return len(client.permissions.intersection(resource_permissions)) > 0