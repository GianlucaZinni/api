import secrets
import string
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from interfaces.clients_interface import ClientsInterface
from interfaces.tokens_interface import TokensInterface
from google_auth_oauthlib.flow import InstalledAppFlow


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
        self,
        client_id: str,
        client_secret: str,
        clients_interface: ClientsInterface,
        tokens_interface: TokensInterface,
    ):
        self.client_id = client_id
        self.client_secret = client_secret
        self.clients_interface = clients_interface
        self.tokens_interface = tokens_interface

    @staticmethod
    def __get_opaque_token(size: int):
        return "".join(
            secrets.choice(string.ascii_letters + string.digits) for i in range(size)
        )

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

        # Configura el flujo de autorización de Google
        flow = InstalledAppFlow.from_client_config(
            {
                "web": {
                    "client_id": self.client_id,
                    "client_secret": self.client_secret,
                    "redirect_uris": ["urn:ietf:wg:oauth:2.0:oob", "http://localhost"],
                }
            },
            scopes=scope if scope else ["openid"],
        )

        # Realiza la solicitud de autenticación
        credentials = flow.run_local_server()
        access_token = credentials.token
        opaque_token = self.__get_opaque_token(token_size)
        expires_in = min(ttl, credentials.expiry - datetime.now())
        expires = self.__calculate_ttl(expires_in.total_seconds())

        self.tokens_interface.put_registry(
            opaque_token, app_id, username, access_token, expires
        )

        return Token(
            access_token=opaque_token,
            expires_in=expires_in,
            type="Bearer",
        )
