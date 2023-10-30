import mysql.connector
from database import db_app

params = db_app.enviroment_variables

class MySQLHandler:
    def __init__(self, database_name=None):
        self.credentials = params["DB_CONFIG"]
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

        for db_name in databases:
            try:
                cursor.execute(f"SHOW DATABASES LIKE '{db_name}'")
                existing_db = cursor.fetchone()

                if existing_db is None:
                    cursor.execute(
                        f"CREATE DATABASE {db_name} CHARACTER SET utf8 COLLATE utf8_unicode_ci"
                    )
                    print(
                        f"Base de datos '{db_name}' creada exitosamente con charset: utf8, collation: utf8_unicode_ci."
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
            result = cursor.fetchall()  # Leer resultados
            return result
        except mysql.connector.Error as err:
            # Manejo de errores
            self.connection.rollback()
        finally:
            cursor.close()


    def get_tables(self):
        query = "SHOW TABLES"
        result = self.query(query)
        if result:
            return [table[0] for table in result]
        return None

    def set_table(self, table_name):
        self.current_table = table_name

    def create_table(
        self,
        table_name,
        partition_key,
        sort_key=None,
        attributes=None,
        ttl_attribute=None,
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

    def get_config_value(self, key):
        query = f"SELECT value FROM config WHERE key = %s", (key,)
        cursor = self.query(query, (key))
        return cursor.fetchone()
