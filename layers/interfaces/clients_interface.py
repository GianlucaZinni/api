from common.common_logging import init_logger
from database.database_handler import DatabaseHandler

# Conexión a la base de datos de MongoDB
db = DatabaseHandler("mongo_votechain")

class ClientsInterface:
    def __init__(self, collection_name, partition_key, sort_key, log_level=None):
        self.collection_name = collection_name
        self.partition_key = partition_key
        self.sort_key = sort_key
        self.logger = init_logger(__name__, log_level)

    def get_item(self, app_id: str, username: str) -> dict:
        # Utiliza el método create_collection para crear la colección si no existe
        db.create_collection(self.collection_name)

        # Luego, realiza la consulta en la colección
        collection = db.db[self.collection_name]
        result = collection.find_one({self.partition_key: app_id, self.sort_key: username})
        
        return result
