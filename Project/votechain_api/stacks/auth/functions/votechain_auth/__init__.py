# from flask import Flask
# # from flask_restplus import Api
# # from api.functions.token.index import Token
# from stacks.database.mysql_handler import create_table

# # api = Api(
# #     title="VoteChain API",
# #     version="1.0",
# # )

# class ApiStack:
#     def __init__(self, app: Flask):
#         self.app = app

#         # Configuración de tablas de base de datos
#         self.tokens_table = create_table(
#             table_name="tokens",
#             partition_key="token",
#             sort_key="app_id",
#             ttl_attribute="expires"
#         )

#         self.clients_table = create_table(
#             table_name="clients",
#             partition_key="app_id",
#             sort_key="username"
#         )

#         self.resources_permissions_table = create_table(
#             table_name="resources_permissions",
#             partition_key="method_resource",
#             sort_key="permission"
#         )

#         self.clients_permissions_table = create_table(
#             table_name="clients_permissions",
#             partition_key="app_id",
#             sort_key="permission"
#         )
