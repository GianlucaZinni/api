from common.common_logging import init_logger
from database.database_handler import DatabaseHandler

# Conexión a la base de datos de MongoDB
db = DatabaseHandler("mongo_votechain")

class ResourcesPermissionsInterface:
    def __init__(self, collection_name, log_level=None):
        self.collection_name = collection_name
        self.logger = init_logger(__name__, log_level)
        self.partition_key = "method_resource"
        self.sort_key = "permission"

    @staticmethod
    def __build_partition_key(method: str, resource: str):
        return f"{method.upper()}_{resource}"

    def get_all_for_resource(self, method: str, resource: str) -> list[dict]:
        # Utiliza el método create_collection para crear la colección si no existe
        db.create_collection(self.collection_name)

        # Luego, realiza la consulta en la colección
        collection = db[self.collection_name]
        query = {self.partition_key: self.__build_partition_key(method, resource)}

        results = list(collection.find(query))

        return results

    def close_connection(self):
        db.close()