import os
import random
import smtplib
import schedule
from datetime import datetime, timedelta
from flask import Blueprint, render_template_string, request, redirect, url_for, flash
from votechain_api.stacks.vote import VoteStack
from votechain_api.stacks.auth import AuthStack
from votechain_api.stacks.auth.models import VotechainUsers
from votechain_api.stacks.vote.models import EmailVerification

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from votechain_api.access import google_login_required, votechain_register_required

auth = AuthStack()
vote = VoteStack()

votacion = Blueprint("Vote-votacion", __name__)

db_session_auth = auth.db_session
db_session_vote = vote.db_session


def build_email_body(year, username, codigo):
    print(f"{os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))}\\template.html")
    with open("G:/GitHub/E-VotingSystem/repos/apigateway/Project/votechain_api/stacks/vote/functions/votacion/template.html", "r", encoding="utf-8") as file:
        body = file.read().replace("[[year]]", str(year))
        body = body.replace("[[username]]", str(username))
        body = body.replace("[[codigo_de_verificacion]]", str(codigo))
        body = body.replace("[[minutos]]", "5")
    return body


def enviar_correo(user_data, codigo):
    correo_emisor = "votechain10@gmail.com"
    contraseña_emisor = "zzal xpue kjhr eqjm"
    correo_destino = user_data.get("email")

    year = datetime.now().year
    mensaje_html = build_email_body(year, user_data.get("name"), codigo)

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

def clean_expired_verification_codes():
    # Función para limpiar códigos de verificación vencidos
    now = datetime.now()
    expired_codes = db_session_vote.query(EmailVerification).filter(EmailVerification.expiration_time <= now).all()
    for code in expired_codes:
        db_session_vote.delete(code)
        db_session_vote.commit()


def generate_verification_code(id):
    while True:
        new_code = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        google_id = db_session_vote.query(EmailVerification).filter_by(google_id=id).first()
        if not google_id:
            existing_code = db_session_vote.query(EmailVerification).filter_by(code=new_code).first()
            if not existing_code:
                expiration_time = datetime.now() + timedelta(seconds=300)
                code = EmailVerification(
                    code=new_code,
                    expiration_time=expiration_time,
                    google_id=id,
                )
                db_session_vote.add(code)
                db_session_vote.commit()
                return code
        return "Ya se te ha enviado un código a tu mail."

schedule.every(5).minutes.do(clean_expired_verification_codes)

@votacion.route("/votechain/vote", methods=["GET", "POST"])
@google_login_required  # Requiere autenticación de Google
@votechain_register_required  # Requiere registro en Votechain
def votar():
    # Crea una cadena de texto HTML de respuesta
    user_data = auth.google.get("userinfo").data
    user = db_session_auth.query(VotechainUsers).filter_by(id=user_data["id"]).first()

    if request.method == "POST":
        verification_code = request.form.get("verification_code")
        existing_code = db_session_vote.query(EmailVerification).filter_by(code=verification_code).first()
        if existing_code and existing_code.google_id == user_data["id"]:
            # Aquí el código es válido, puedes redirigir al usuario a la página de votación realizada
            db_session_vote.delete(existing_code)
            db_session_vote.commit()
            response_html = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Votación realizada</title>
            </head>
            <body>
                <h1>Felicidades, ya votaste!</h1>
            </body>
            </html>
            """

            return render_template_string(response_html, user=user)
        else:
            flash("Código de verificación no válido", "error")

    # Genera y envía un código de verificación al usuario
    verification_code = generate_verification_code(user_data["id"])
    if isinstance(verification_code, EmailVerification):
        print("Usuario: ", user.__dict__)
        enviar_correo(user.__dict__, verification_code.code)

    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>VOTECHAIN - EMAIL VERIFICATION</title>
    </head>
    <body>
        <h1>Se te ha enviado un código por email, ingrésalo a continuación</h1>
        <form method="POST">
            <input type="text" name="verification_code" placeholder="Código de verificación" required>
            <button type="submit">Verificar</button>
        </form>
    </body>
    </html>
    """)