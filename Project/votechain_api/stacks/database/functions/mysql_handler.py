import mysql.connector
import json

# from layers.utils.tools import load_credentials

params_route = "Project/params/develop.json"

import json


def load_credentials(credentials_file):
    with open(credentials_file, "r") as file:
        return json.load(file)


class MySQLDatabaseHandler:
    def __init__(self, database_name=None):
        self.credentials = load_credentials(params_route)["DB_CONFIG"]
        self.database_name = database_name
        self.connection = self.connect()
        self.base_creation()

    def connect(self):
        try:
            if self.database_name:
                connection = mysql.connector.connect(
                    host=self.credentials["GENERAL"]["HOST"],
                    user=self.credentials["GENERAL"]["USERNAME"],
                    password=self.credentials["GENERAL"]["PASSWORD"],
                    database=self.database_name,
                )
                return connection

            else:
                connection = mysql.connector.connect(
                    host=self.credentials["GENERAL"]["HOST"],
                    user=self.credentials["GENERAL"]["USERNAME"],
                    password=self.credentials["GENERAL"]["PASSWORD"],
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

    def base_creation(self):
        cursor = self.connection.cursor()

        databases = self.credentials[
            "DATABASES"
        ]  # lista de bases de datos desde el JSON

        for db_name, db_config in databases.items():
            charset = db_config.get(
                "charset", "utf8"
            )  # Usa el charset o usa un valor predeterminado si no está definido
            collation = db_config.get(
                "collation", "utf8_unicode_ci"
            )  # Usa la collation o usa un valor predeterminado si no está definido

            try:
                cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
                existing_db = cursor.fetchone()

                if existing_db is None:
                    cursor.execute(
                        f"CREATE DATABASE {db_name} CHARACTER SET {charset} COLLATE {collation}"
                    )
                    print(
                        f"Base de datos '{db_name}' creada exitosamente con charset: {charset}, collation: {collation}."
                    )
                else:
                    return
            except mysql.connector.Error as err:
                print(f"Error al crear la base de datos '{db_name}': {err}")

        cursor.close()
        self.connection.close()

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
        if cursor:
            return [table[0] for table in cursor]
        return None

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


    def create_table(
        self, table_name, partition_key, sort_key=None, attributes=None, ttl_attribute=None
    ):
        # Check if the table already exists
        check_tables = self.get_tables()
        if not check_tables or not table_name in check_tables:
            # Define la estructura de la tabla en SQL
            create_table_query = f"""
                CREATE TABLE {table_name} (
                    {partition_key} VARCHAR(255) PRIMARY KEY,
                """

            # Add the sort key (if specified)
            if sort_key:
                create_table_query += f"{sort_key} VARCHAR(255),"

            # Add TTL attribute (if specified)
            if ttl_attribute:
                create_table_query += f"{ttl_attribute} DATETIME,"

            # Add attributes (if specified)
            if attributes:
                for name in attributes:
                    create_table_query += f"{name} VARCHAR(255),"

            # Remove the trailing comma if it exists
            if create_table_query.endswith(","):
                create_table_query = create_table_query[:-1]

            # Close the CREATE TABLE statement
            create_table_query += ");"

            # Execute the query to create the table
            self.query(create_table_query)
            print(f"Table '{table_name}' created successfully.")

    def get_config_value(self, key):
        query = f"SELECT value FROM config WHERE key = %s", (key,)
        cursor = self.query(query, (key))
        return cursor.fetchone()
