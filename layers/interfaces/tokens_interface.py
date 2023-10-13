from datetime import datetime
from common.common_logging import init_logger
from database.database_handler import DatabaseHandler

# Conexión a la base de datos de MongoDB
db = DatabaseHandler("mongo_votechain")


class TokensInterface:
    def __init__(self, collection_name, log_level=None):
        self.collection_name = collection_name
        self.logger = init_logger(__name__, log_level)
        self.partition_key = "token"
        self.sort_key = "app_id"

    def get_item(self, token: str, app_id: str) -> dict:
        # Utiliza el método create_collection para crear la colección si no existe
        db.create_collection(self.collection_name)

        # Luego, realiza la consulta en la colección
        collection = db[self.collection_name]
        query = {self.partition_key: token, self.sort_key: app_id}

        result = collection.find_one(query)
        return result

    def get_items_by_partition_key(self, token: str):
        # Utiliza el método create_collection para crear la colección si no existe
        db.create_collection(self.collection_name)

        # Luego, realiza la consulta en la colección
        collection = db[self.collection_name]
        query = {self.partition_key: token}

        results = list(collection.find(query))
        return results

    def put_registry(self, token: str, app_id: str, username: str, access_token_aad: str, expires: int) -> None:
        # Utiliza el método create_collection para crear la colección si no existe
        db.create_collection(self.collection_name)

        # Luego, inserta los datos en la colección
        collection = db[self.collection_name]
        record = {
            self.partition_key: token,
            self.sort_key: app_id,
            "username": username,
            "access_token_aad": access_token_aad,
            "creation_date": datetime.now().isoformat(),
            "expires": expires,
        }

        collection.insert_one(record)

    def close_connection(self):
        db.close_connection()
