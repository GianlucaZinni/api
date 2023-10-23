from common.common_logging import init_logger
from database.mysql_handler import MySQLDatabaseHandler

# Inicializa la conexión a la base de datos MySQL
db = MySQLDatabaseHandler()

class ClientsPermissionsInterface:
    def __init__(self, table_name, log_level=None):
        self.table_name = table_name
        self.logger = init_logger(__name__, log_level)
        self.partition_key = "app_id"  # Asegúrate de que coincida con tu estructura de tabla en MySQL
        self.sort_key = "permission"  # Asegúrate de que coincida con tu estructura de tabla en MySQL

    def get_all_for_client(self, app_id: str) -> list[dict]:
        # Establece la tabla en la que realizarás la operación
        db.set_table(self.table_name)

        # Realiza la consulta en la tabla
        query = f"SELECT * FROM {self.table_name} WHERE {self.partition_key} = %s"
        results = db.query_items(query, (app_id,))

        return results
