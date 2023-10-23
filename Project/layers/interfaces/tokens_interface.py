from datetime import datetime
from common.common_logging import init_logger
from database.mysql_handler import MySQLDatabaseHandler

# Inicializa la conexión a la base de datos MySQL
db = MySQLDatabaseHandler()

class TokensInterface:
    def __init__(self, table_name, log_level=None):
        self.table_name = table_name
        self.logger = init_logger(__name__, log_level)
        self.partition_key = "token"  # Asegúrate de que coincida con tu estructura de tabla en MySQL
        self.sort_key = "app_id"  # Asegúrate de que coincida con tu estructura de tabla en MySQL

    def get_item(self, token: str, app_id: str) -> dict:

        # Realiza la consulta en la tabla
        query = f"SELECT * FROM {self.table_name} WHERE {self.partition_key} = %s AND {self.sort_key} = %s"
        results = db.query_items(query, (token, app_id))

        # Si se encuentra un registro, devuelve el primer resultado
        if results:
            return results[0]
        return None

    def get_items_by_partition_key(self, token: str):
        # Realiza la consulta en la tabla
        query = f"SELECT * FROM {self.table_name} WHERE {self.partition_key} = %s"
        results = db.query_items(query, (token))

        return results

    def put_registry(self, token: str, app_id: str, username: str, access_token_aad: str, expires: int) -> None:
        # Inserta los datos en la tabla
        query = f"INSERT INTO {self.table_name} ({self.partition_key}, {self.sort_key}, username, access_token_aad, creation_date, expires) VALUES (%s, %s, %s, %s, %s, %s)"
        creation_date = datetime.now().isoformat()
        db.query(query, (token, app_id, username, access_token_aad, creation_date, expires))