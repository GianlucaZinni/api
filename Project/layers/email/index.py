import os
import smtplib
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def build_email_body(year, username, codigo):
    with open(f"{os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))}\\email\\template.html", "r", encoding="utf-8") as file:
        body = file.read().replace("[[year]]", str(year))
        body = body.replace("[[username]]", str(username))
        body = body.replace("[[codigo_de_verificacion]]", str(codigo))
        body = body.replace("[[minutos]]", "5")
    return body


def enviar_correo(votechain_data, google_data, codigo):
    correo_emisor = os.getenv("EMIT_EMAIL")
    contraseña_emisor = os.getenv("EMIT_PASSWORD")
    correo_destino = google_data.email

    year = datetime.now().year
    mensaje_html = build_email_body(year, votechain_data.nombre, codigo)

    # Crear el mensaje Multipart
    mensaje = MIMEMultipart()
    mensaje["From"] = correo_emisor
    mensaje["To"] = correo_destino
    mensaje["Subject"] = "Código de verificación - Votechain"

    # Crear una parte de texto en formato HTML
    mensaje_html = MIMEText(mensaje_html, "html")

    # Adjuntar la parte HTML al mensaje
    mensaje.attach(mensaje_html)

    # Configuración de los datos del servidor SMTP y cuenta de correo emisora
    servidor_smtp = "smtp.gmail.com"
    puerto_smtp = 587
    server = smtplib.SMTP(servidor_smtp, puerto_smtp)
    server.starttls()

    # Iniciar sesión en tu cuenta de Gmail
    server.login(correo_emisor, contraseña_emisor)

    # Enviar el correo
    server.sendmail(correo_emisor, correo_destino, mensaje_html.as_string())

    # Cerrar la conexión
    server.quit()
