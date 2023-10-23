import mysql.connector
import json
import os

class MySQLDatabaseHandler:
    def __init__(self):
        self.credentials = self.load_credentials(f"{os.path.dirname(os.path.realpath(__file__))}/database_creds.json")
        self.connection = self.connect()

    def load_credentials(self, credentials_file):
        with open(credentials_file, "r") as file:
            return json.load(file)

    def connect(self):
        try:
            connection = mysql.connector.connect(
                host=self.credentials["host"],
                user=self.credentials["user"],
                password=self.credentials["password"],
                database=self.credentials["database"]
            )
            return connection
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return None

    def disconnect(self):
        if self.connection is not None and self.connection.is_connected():
            self.connection.disconnect()

    def check_connection(self):
        if self.connection is not None and self.connection.is_connected():
            return True
        return False

    def query(self, query, data=None):
        if not self.check_connection():
            self.connect()
        cursor = self.connection.cursor()
        try:
            if data:
                cursor.execute(query, data)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            self.connection.rollback()
        finally:
            cursor.close()

    def get_tables(self):
        query = "SHOW TABLES"
        cursor = self.query(query)
        return [table[0] for table in cursor]

    def set_table(self, table_name):
        self.current_table = table_name

    def get_item(self, key):
        query = f"SELECT * FROM {self.current_table} WHERE id = %s"
        cursor = self.query(query, (key,))
        return cursor.fetchone()

    def set_item(self, key, data):
        query = f"INSERT INTO {self.current_table} (id, data) VALUES (%s, %s)"
        self.query(query, (key, data))

    def query_items(self, query):
        cursor = self.query(query)
        return cursor.fetchall()

    def update_item(self, key, data):
        query = f"UPDATE {self.current_table} SET data = %s WHERE id = %s"
        self.query(query, (data, key))

    def get_config_value(self, key):
        query = f"SELECT value FROM config WHERE key = %s", (key,)
        cursor = self.query(query, (key))
        return cursor.fetchone()

if __name__ == "__main__":
    # Carga las credenciales desde el archivo JSON
    db = MySQLDatabaseHandler()