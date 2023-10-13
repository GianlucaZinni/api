import secrets
import string
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from layers.interfaces.clients_interface import ClientsInterface
from layers.interfaces.tokens_interface import TokensInterface
from msal import PublicClientApplication


@dataclass
class Token:
    access_token: str
    expires_in: int
    type: str


class UnauthorizedClientException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class AcquireTokenException(Exception):
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class TokenFactory:
    def __init__(
        self, tenant_id: str, client_id: str, clients_interface: ClientsInterface, tokens_interface: TokensInterface
    ):
        self.authority = f"https://login.microsoftonline.com/{tenant_id}"
        self.app = PublicClientApplication(client_id=client_id, authority=self.authority)
        self.default_scope = [f"{client_id}/.default"]
        self.clients_interface = clients_interface
        self.tokens_interface = tokens_interface

    @staticmethod
    def __get_opaque_token(size: int):
        return "".join(secrets.choice(string.ascii_letters + string.digits) for i in range(size))

    @staticmethod
    def __calculate_ttl(seconds: int) -> int:
        ttl_date_time = datetime.now() + timedelta(seconds=seconds)
        return int(ttl_date_time.timestamp())

    def create(
        self,
        username: str,
        password: str,
        app_id: str,
        *,
        token_size: int = 128,
        ttl: int = 300,
        scope: Optional["list[str]"] = None,
    ) -> Token:

        if not self.clients_interface.get_item(app_id, username):
            raise UnauthorizedClientException(
                f"No se encontró registrada la appId: {app_id} para el usuario {username}"
            )

        acquire_tokens_result = self.app.acquire_token_by_username_password(
            username=username, password=password, scopes=scope if scope else self.default_scope
        )

        if "error" in acquire_tokens_result:
            raise AcquireTokenException(
                "Se produjo un error al obtener el token. Message: "
                f"{acquire_tokens_result.get('error')}. Description:{acquire_tokens_result.get('error_description')}",
            )

        access_token_aad = acquire_tokens_result["access_token"]
        opaque_token = self.__get_opaque_token(token_size)
        expires_in = min(ttl, acquire_tokens_result["expires_in"])
        expires = self.__calculate_ttl(expires_in)

        self.tokens_interface.put_registry(opaque_token, app_id, username, access_token_aad, expires)

        return Token(
            access_token=opaque_token,
            expires_in=expires_in,
            type="Bearer",
        )
