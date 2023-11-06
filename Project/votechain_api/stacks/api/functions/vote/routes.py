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
from Project.votechain_api.stacks.controller.functions.email.index import (
    clean_expired_verification_codes,
    get_email_code,
    post_email_code,
)
from Project.votechain_api.stacks.controller.functions.vote.index import post_audit_vote, get_candidatos, get_partidos_politicos
from votechain_api.access import (
    google_login_required,
    votechain_register_required,
    verify_actually_audit,
    verify_actually_vote
)
import requests
import json


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

    # Renderizar la plantilla HTML con los partidos
    return render_template("votaciones/candidatos.html", partidos=partidos)


@vote.route("/votechain/votar", methods=["POST"])
@google_login_required
@votechain_register_required
@verify_actually_vote
def votar(votechain_user, google_user):
    try:
        candidato_votado = request.form.get("voto")
        if candidato_votado:
            candidato_votado = json.loads(candidato_votado.replace("'", "\""))
            voto = {
                "lista": candidato_votado.get("lista"),
                "partido": candidato_votado.get("partido_politico")
            }
            response = requests.post("http://127.0.0.1:8000/registrar_voto", json=voto)
            if response.status_code == 200:
                post_audit_vote(votechain_user)
                return redirect(url_for("API-VOTE.votado"))
            else:
                raise Exception("Error al registrar el voto.")
        else:
            raise ValueError("No se recibió información de voto.")
    except Exception as e:
        return f"Error: {e}"
        

@vote.route("/votechain/votado", methods=["GET"])
@google_login_required
@votechain_register_required
def votado(votechain_user, google_user):
    # Renderizar el formulario
    return render_template("votaciones/felicitaciones.html")