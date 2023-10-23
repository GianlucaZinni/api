import mysql.connector
from utils.tools import load_credentials
import os

def create_mysql_db(database_name):

    database_creds = load_credentials(f"{os.path.dirname(os.path.realpath(__file__))}/database_creds.json")

    # Define las credenciales de MySQL
    mysql_config = {
        "host": database_creds["host"],
        "user": database_creds["user"],
        "password": database_creds["password"]
    }

    # Conéctate al servidor de MySQL
    connection = mysql.connector.connect(**mysql_config)
    cursor = connection.cursor()

    try:
        # Crea la base de datos si no existe
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"Base de datos {database_name} creada con éxito.")
    except mysql.connector.Error as err:
        print(f"Error al crear la base de datos: {err}")
    finally:
        cursor.close()
        connection.close()