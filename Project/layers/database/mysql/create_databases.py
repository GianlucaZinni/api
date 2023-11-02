import mysql.connector
import os

def create_databases():
    # Conectarse a la base de datos MySQL
    connection = mysql.connector.connect(
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
    )

    cursor = connection.cursor()

    # Leer el archivo SQL
    with open(f"{os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))}\mysql\create_databases.sql", "r", encoding="utf-8") as file:
        sql_script = file.read()

    # Dividir el script en comandos individuales
    sql_commands = sql_script.split(";")

    # Ejecutar cada comando SQL
    for command in sql_commands:
        if command.strip():
            try:
                cursor.execute(command)
            except mysql.connector.Error as err:
                if err.errno == 1050:  # Código de error 1050 indica que la tabla ya existe
                    pass
                else:
                    print(f"Error al ejecutar el comando SQL: {command}")
                    print(err)


    # Confirmar los cambios y cerrar la conexión
    connection.commit()
    cursor.close()
    connection.close()
