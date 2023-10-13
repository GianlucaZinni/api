import mysql.connector
import json
from pymongo import MongoClient

class DatabaseHandler:
    def __init__(self, database_name):
        self.client = MongoClient("localhost", 27017)  # Ajusta la conexión según tu configuración
        self.db = self.client[database_name]

    def create_collection(self, collection_name):
        if collection_name not in self.db.list_collection_names():
            self.db.create_collection(collection_name)
            print(f"Colección '{collection_name}' creada con éxito en MongoDB.")

    def close_connection(self):
        self.client.close()

class DatabaseHandler2:
    def __init__(self, credentials_file):
        with open(credentials_file, "r") as file:
            credentials = json.load(file)

        self.connection = mysql.connector.connect(
            host=credentials["host"],
            user=credentials["user"],
            password=credentials["password"],
            database=credentials["database"]
        )

    def create_table(self, table_name, attributes):
        cursor = self.connection.cursor()

        # Verificar si la tabla ya existe
        cursor.execute(f"SHOW TABLES LIKE '{table_name}'")
        if not cursor.fetchone():
            # La tabla no existe, entonces la creamos
            attribute_definitions = ", ".join([f"{attribute['attribute_name']} {attribute['attribute_type']}" for attribute in attributes])
            query = f"CREATE TABLE {table_name} ({attribute_definitions})"
            cursor.execute(query)

        cursor.close()

    def close_connection(self):
        self.connection.close()

if __name__ == "__main__":
    # Carga las credenciales desde el archivo JSON
    db = DatabaseHandler(credentials_file="develop.json")

    # Define la estructura de la tabla (nombre, atributos y sort key)
    table_name = "example_table"
    table_attributes = [
        {"attribute_name": "app_id", "attribute_type": "VARCHAR(255)"},
        {"attribute_name": "username", "attribute_type": "VARCHAR(255)"},
        {"attribute_name": "age", "attribute_type": "INT"},
    ]

    # Crea la tabla si no existe
    db.create_table(table_name, table_attributes)

    # Cierra la conexión a la base de datos
    db.close_connection()
