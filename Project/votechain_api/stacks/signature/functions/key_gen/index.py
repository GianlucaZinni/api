from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_public_key, load_pem_private_key
from cryptography.hazmat.primitives import serialization as crypto_serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.backends import default_backend as crypto_default_backend

app = Flask(__name__)

# Genera un par de claves para un usuario y guárdalas en archivos o en una base de datos
def generar_par_claves():
    key = rsa.generate_private_key(
        backend=crypto_default_backend(),
        public_exponent=65537,
        key_size=2048
    )

    private_key = key.private_bytes(
        crypto_serialization.Encoding.PEM,
        crypto_serialization.PrivateFormat.PKCS8,
        crypto_serialization.NoEncryption()
    )
    

    public_key = key.public_key().public_bytes(
        crypto_serialization.Encoding.OpenSSH,
        crypto_serialization.PublicFormat.OpenSSH
    )
    
    return private_key, public_key


    # Guarda las claves en archivos o base de datos

# Obtiene claves para un usuario (deberías implementar la lógica de autenticación)
def obtener_par_claves_para_usuario(usuario_id):
    # Recupera las claves desde donde las hayas guardado
    pass

# Firmar un mensaje
def firmar_mensaje(mensaje, clave_privada):
    mensaje = mensaje.encode('utf-8')
    firma = clave_privada.sign(
        mensaje,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return firma

# Verificar una firma
def verificar_firma(mensaje, firma, clave_publica):
    mensaje = mensaje.encode('utf-8')
    try:
        clave_publica.verify(
            firma,
            mensaje,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except cryptography.exceptions.InvalidSignature:
        return False

@app.route('/enviar_mensaje', methods=['POST'])
def enviar_mensaje():
    datos = request.json
    mensaje = datos['mensaje']
    firma = datos['firma']
    emisor_id = datos['emisor']
    receptor_id = datos['receptor']

    # Obtener claves del emisor y receptor
    clave_privada_emisor = obtener_par_claves_para_usuario(emisor_id)['privada']
    clave_publica_receptor = obtener_par_claves_para_usuario(receptor_id)['publica']

    # Verificar la firma
    if verificar_firma(mensaje, firma, clave_publica_receptor):
        # La firma es válida, el mensaje proviene del emisor correcto

        # Cifrar el mensaje para el receptor
        mensaje_cifrado = cifrar_mensaje(mensaje, clave_publica_receptor)

        # Envía el mensaje cifrado al receptor o haz lo que necesites con él
        # ...

        return jsonify({"mensaje_cifrado": mensaje_cifrado, "estado": "Mensaje enviado"})
    else:
        return jsonify({"estado": "Firma inválida"})

if __name__ == '__main__':
    app.run(debug=True)
