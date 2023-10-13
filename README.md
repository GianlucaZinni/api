Configuración del proyecto
Env con Python, Flask y MySQL.

Se debe configurar SSL en producción, ya que transmitirá información de autenticación confidencial a través de Internet. (NGINX o Apache).

MySQL DB Setup

Asegúrate de haber configurado previamente un servidor MySQL y tener acceso a una base de datos. 
A continuación, se proporcionan instrucciones SQL para crear la base de datos authdb_dev, así como las tablas clients y blacklist:

1. Crear la base de datos:

CREATE DATABASE authdb_dev;

2. Crear un usuario y asignar permisos:
Puedes crear un usuario para la base de datos y asignarle permisos. Asegúrate de reemplazar 'tu_usuario' y 'tu_contrasena' con los valores adecuados.

CREATE USER 'tu_usuario'@'localhost' IDENTIFIED BY 'tu_contrasena';
GRANT ALL PRIVILEGES ON authdb_dev.* TO 'tu_usuario'@'localhost';
FLUSH PRIVILEGES;

3. Utilizar la base de datos:

Antes de crear tablas, asegúrate de utilizar la base de datos authdb_dev:

USE authdb_dev;

4. Crear la tabla clients:

CREATE TABLE clients (
    Id INT AUTO_INCREMENT PRIMARY KEY,
    ClientId VARCHAR(128) NOT NULL,
    ClientSecret VARCHAR(256) NOT NULL,
    IsAdmin BOOLEAN NOT NULL,
    UNIQUE (ClientId)
);

5. Crear la tabla blacklist:

CREATE TABLE blacklist (
    token VARCHAR(256) NOT NULL
);

Estos scripts SQL crean la base de datos authdb_dev, una tabla clients con una restricción UNIQUE en la columna ClientId, y una tabla blacklist para almacenar tokens. Asegúrate de ajustar las configuraciones de usuario y contraseña según tus necesidades y asegurarte de que tu servidor MySQL esté en funcionamiento antes de ejecutar estos comandos.

Configuración de la aplicación
pip install flask psycopg2 pyjwt python-dotenv