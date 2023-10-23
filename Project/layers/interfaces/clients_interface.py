from common.common_logging import init_logger
from database.mysql_handler import MySQLDatabaseHandler

# Conexión a la base de datos de MongoDB
db = MySQLDatabaseHandler()

class ClientsInterface:
    def __init__(self, table_name, log_level=None):
        self.table_name = table_name
        self.logger = init_logger(__name__, log_level)
        self.partition_key = "app_id"
        self.sort_key = "username"

    def get_item(self, app_id: str, username: str) -> dict:
        # Realiza la consulta para obtener el elemento
        result = db.get_item(key=(app_id, username))

        return result