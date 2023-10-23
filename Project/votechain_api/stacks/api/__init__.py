from flask import Flask
# from flask_restplus import Api
# from api.functions.token.index import Token
from votechain_layers.persistence.create_schemas import create_table

# api = Api(
#     title="VoteChain API",
#     version="1.0",
# )

class ApiStack:
    def __init__(self, app: Flask):
        self.app = app

        # Configuración de tablas de base de datos
        self.tokens_table = create_table(
            table_name="tokens",
            partition_key="token",
            sort_key="app_id",
            ttl_attribute="expires"
        )

        self.clients_table = create_table(
            table_name="clients",
            partition_key="app_id",
            sort_key="username"
        )

        self.resources_permissions_table = create_table(
            table_name="resources_permissions",
            partition_key="method_resource",
            sort_key="permission"
        )

        self.clients_permissions_table = create_table(
            table_name="clients_permissions",
            partition_key="app_id",
            sort_key="permission"
        )
        # self.configure_database_tables()

        # Configuración de modelos
        # self.token_model = api.model(
        #     self,
        #     "api-token-model",
        #     {
        #         "access_token": fields.String(required=True),
        #         "token_type": fields.String(required=True),
        #         "expires_in": fields.Integer(required=True),
        #     }
        # )
        
        # api.add_namespace(Token)
        

# Importa y registra los espacios de nombres de tus recursos aquí
# from .functions.token.resources import ns as token_ns
"""
Espacios de nombres
Los espacios de nombres son opcionales y añaden un toque organizativo adicional a la API, principalmente, desde el punto de vista de la documentación. Un espacio de nombres le permite agrupar recursos relacionados bajo una raíz común y es fácil de crear:
ns_conf = api.namespace('conferences', description='Conference operations')
"""
# api.add_namespace(token_ns)

# Puedes hacer lo mismo para otros recursos
