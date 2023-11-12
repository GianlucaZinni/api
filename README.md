# Proyecto Votechain

¡Bienvenido al Proyecto Votechain! Este proyecto es una aplicación que simula un servicio de votación electrónica segura.

## Instalación del entorno

1. Clona el repositorio en tu máquina local:

   ```bash
   git clone https://github.com/GianlucaZinni/api
    ```

2. Navega al directorio del proyecto Votechain API:

    ```bash
    cd api
    ```

3. Crea un entorno virtual (se recomienda utilizar `venv`):

    ```bash
    python -m venv venv
    ```

4. Activa el entorno virtual:

    En Windows desde CMD
    ```bash
    .\venv\Scripts\activate
    ```

    En Linux/macOS
    ```bash
    source venv/bin/activate
    ```

4. Instala las dependencias del proyecto desde el archivo `requirements.txt`:
    
        ```bash
        pip install -r requirements.txt
        ```

## Configurar la aplicación
En la carpeta principal `Project` se encuentra el archivo `.env` que contiene las variables a modificar:

`DATABASE_URI`

`MYSQL_HOST`

`MYSQL_USER`

`MYSQL_PASSWORD`

## Iniciar la aplicación

Una vez que el entorno esté configurado, puedes iniciar la aplicación ejecutando el archivo run.py.
Este archivo se encargará de generar y llenar las bases de datos, además de iniciar los servicios de Front End y API a través de FLASK.
    
    ```bash
    python run.py
    ```

# Configuración adiciona en ´run.py´	
Dentro del archivo run.py, encontrarás una función llamada create_renaper_data. Esta función tiene un parámetro booleano que determina si se deben crear registros falsos en la base de datos RENAPER. Por defecto, está configurado en False. Si deseas crear registros falsos, simplemente cambia el valor a True:
        
        ```python
        create_renaper_data(True) # Si es True, crea 50 registros falsos en la base de datos RENAPER
        ```

¡Listo! Ahora estás listo para disfrutar de la aplicación Votechain. Si tienes alguna pregunta o problema, no dudes en ponerte en contacto con nosotros. ¡Diviértete explorando!