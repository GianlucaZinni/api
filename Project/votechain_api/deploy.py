import subprocess


# Definir los comandos para ejecutar los microservicios en diferentes terminales
microservices = [
    # "python votechain_apigateway/stacks/functions/profiles/app.py",
    "python project/votechain_api/stacks/client/functions/google_auth/index.py",
    # "python votechain_apigateway/stacks/functions/recipes/app.py",
]

# Iniciar la puerta de enlace de API
api_gateway_cmd = "python project/votechain_api/app.py"

# Crear procesos para ejecutar los microservicios en terminales separadas
processes = [subprocess.Popen(cmd, shell=True) for cmd in microservices]

# Iniciar la puerta de enlace de la API en el proceso principal
subprocess.run(api_gateway_cmd, shell=True)

# Esperar a que todos los procesos se completen
for process in processes:
    process.wait()
