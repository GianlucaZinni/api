from flask import Blueprint, render_template_string, request, redirect, url_for, jsonify, session
from votechain_api.stacks.api import api
from Project.votechain_api.stacks.controller.functions.email.index import clean_expired_verification_codes, get_email_code, post_email_code
from votechain_api.access import google_login_required, votechain_register_required

vote = Blueprint("API-VOTE", __name__)

@vote.route("/votechain/validar_codigo", methods=["GET", "POST"])
@google_login_required
@votechain_register_required
def validar_codigo(votechain_user, google_user):
    
    clean_expired_verification_codes()
    
    code = get_email_code(votechain_user, google_user)
    if request.method == "POST":
        response = post_email_code(votechain_user, google_user, code, code.tries, request.form.get("verification_code"))

        if response == "success":
            return redirect(url_for("API-VOTE.candidatos"))
            
        elif response == "invalid":
            api.message_email = code.tries
            return redirect(url_for("API-VOTE.validar_codigo"))
        
        elif response == "no-tries":
            session.clear()
            return redirect(url_for("API-GOOGLE_AUTH.index"))

    # Genera y envía un código de verificación al usuario
    if code:
        api.message_email = code.tries
        
    html = """
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
        <p> {{ message }} </p>
    </body>
    </html>
    """

    return render_template_string(html, message=api.message_email)


@vote.route("/votechain/candidatos", methods=["GET"])
@google_login_required
@votechain_register_required
def candidatos(votechain_user, google_user):
    # Crear el formulario HTML con tres botones
    form_html = """
    <form method="POST" action="/votechain/votar">
        <button type="submit" name="voto" value="candidato1">Votar por Candidato 1</button>
        <button type="submit" name="voto" value="candidato2">Votar por Candidato 2</button>
        <button type="submit" name="voto" value="candidato3">Votar por Candidato 3</button>
    </form>
    """

    # Renderizar el formulario
    return render_template_string(form_html)


@vote.route("/votechain/votar", methods=["POST"])
@google_login_required
@votechain_register_required
def votar(votechain_user, google_user):
    # Recibir y procesar los datos del formulario
    candidato_votado = request.form.get("voto")

    # Puedes imprimir o manejar los datos del candidato votado
    print(f"Usuario {votechain_user.DNI} votó por {candidato_votado}")

    # Realizar más acciones según el candidato votado

    # Devolver una respuesta al usuario
    return jsonify({"message": "Voto registrado exitosamente"})
