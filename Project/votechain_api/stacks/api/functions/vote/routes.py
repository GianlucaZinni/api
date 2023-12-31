from flask import (
    Blueprint,
    render_template,
    render_template_string,
    request,
    redirect,
    url_for,
    session,
)
from votechain_api.stacks.api import api
from votechain_api.stacks.controller.functions.email.index import (
    clean_expired_verification_codes,
    get_email_code,
    post_email_code,
)
from votechain_api.stacks.controller.functions.vote.index import post_audit_vote, get_candidatos, get_partidos_politicos
from votechain_api.access import (
    google_login_required,
    votechain_register_required,
    verify_actually_audit,
    verify_actually_vote
)
import requests
import json
import os


vote = Blueprint("API-VOTE", __name__)


@vote.route("/votechain/validar_codigo", methods=["GET", "POST"])
@google_login_required
@votechain_register_required
@verify_actually_audit
def validar_codigo(votechain_user, google_user):
    clean_expired_verification_codes()

    code = get_email_code(votechain_user, google_user)
    if request.method == "POST":
        response = post_email_code(
            votechain_user, google_user, code, request.form.get("verification_code")
        )

        if response == "success":
            return redirect(url_for("API-VOTE.candidatos"))

        elif response == "invalid":
            api.message_email = (
                f"Nro de trámite inválido. Cantidad de intentos restantes {code.tries}"
            )
            return redirect(url_for("API-VOTE.validar_codigo"))

        elif response == "no-tries":
            session.clear()
            return redirect(url_for("API-VOTE_AUTH.exceeded_tries"))

    # Genera y envía un código de verificación al usuario
    if code:
        api.message_email = code.tries

    return render_template("votaciones/verificar_email.html", message=api.message_email)


@vote.route("/votechain/candidatos", methods=["GET"])
@google_login_required
@votechain_register_required
@verify_actually_vote
def candidatos(votechain_user, google_user):
    # Crear el formulario HTML con tres botones
    
    
# Ejemplo de cómo obtener candidatos y sus partidos
    candidatos = get_candidatos()
    partidos = []
    for candidato in candidatos:
        partido_politico = get_partidos_politicos(candidato)[0]
        info_partido = {
            "partido_politico": partido_politico.nombre,
            "siglas": partido_politico.siglas,
            "lista": partido_politico.lista,
            "presidente": candidato.nombre_presidente + " " + candidato.apellido_presidente,
            "vicepresidente": candidato.nombre_vicepresidente + " " + candidato.apellido_vicepresidente,
            "imagen_boleta": candidato.foto_url,
            "imagen_logo": partido_politico.logo_url,
            "partido_id": partido_politico.partido_id,
            "candidatos_id": candidato.candidatos_id
        }

        partidos.append(info_partido)

    
    form_html = """
        <form method="POST" action="/votechain/votar">

    """
    for partido_politico in partidos:
        form_html += f"""
        <button type="submit" name="voto" value="{partido_politico}">Votar por {partido_politico.get("partido_politico")}</button>
        """
        
    form_html += """
        </form>
        """

    # Renderizar el formulario
    return render_template_string(form_html)


@vote.route("/votechain/votar", methods=["POST"])
@google_login_required
@votechain_register_required
@verify_actually_vote
def votar(votechain_user, google_user):
    # Recibir y procesar los datos del formulario
    candidato_votado = json.loads(request.form.get("voto").replace("'", "\""))

    if request.method == "POST":
        message = {
            "token": os.getenv("SECRET_TOKEN"),
            "voto": { 
                "lista": candidato_votado.get("lista"),
                "partido": candidato_votado.get("partido_politico")
            }
        }


        print(message)
        
        # Realizar el POST a la ruta especificada
        response = requests.post("http://127.0.0.1:8000/registrar_voto", json=message)
        print(response.text)
        # Comprobar si la solicitud POST fue exitosa
        if response.status_code == 200:
            post_audit_vote(votechain_user)
            # Si la solicitud fue exitosa, puedes redirigir al usuario a la página deseada
            return redirect(url_for("API-VOTE.votado"))
        else:
            # Si la solicitud falló, puedes manejar el error de alguna manera
            # Por ejemplo, puedes mostrar un mensaje de error o redirigir a una página de error
            return "Error al registrar el voto. Por favor, inténtalo de nuevo."
        

@vote.route("/votechain/votado", methods=["GET"])
@google_login_required
@votechain_register_required
def votado(votechain_user, google_user):
    # Renderizar el formulario
    return render_template("votaciones/felicitaciones.html")