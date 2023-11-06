from flask import (
    redirect,
    render_template,
    url_for,
    render_template_string,
    Blueprint,
    jsonify,
    request,
    session,
)
from votechain_api.stacks.api import api
from votechain_api.access import (
    google_login_required,
    votechain_register_required,
)
from votechain_api.stacks.controller.functions.renaper.index import (
    verificar_en_padron,
    obtener_individuo_renaper,
)
from votechain_api.stacks.controller.functions.vote_auth.index import (
    check_already_register,
    check_dni_already_exists,
    insert_into_votechain,
    post_nro_tramite,
)

vote_auth = Blueprint("API-VOTE_AUTH", __name__)


@vote_auth.route("/votechain/register", methods=["GET", "POST"])
@google_login_required
def register(google_user):
    if check_already_register(google_user):
        return redirect(url_for("API-VOTE_AUTH.persona_info"))

    if request.method == "POST":
        persona_data = request.form
        try:
            dni = int(persona_data.get("dni", "").strip())
        except ValueError:
            return jsonify({"error": "DNI debe ser un número."}), 400

        nombre = persona_data.get("nombre", "").strip()
        apellido = persona_data.get("apellido", "").strip()
        telefono = persona_data.get("telefono", "").strip()

        if not nombre or not apellido:
            return jsonify({"error": "Nombre y apellido son obligatorios."}), 400
        
        if not persona_data:
            return jsonify({"error": "No data sent."}), 400

        verification_result = verificar_en_padron(persona_data)

        if verification_result:
            if not check_dni_already_exists(persona_data):
                insert_into_votechain(persona_data, google_user.id_google)

                return redirect(url_for("API-VOTE_AUTH.persona_info"))

            return (
                jsonify(
                    {
                        "message": "El DNI ya está registrado a una cuenta de email distinta."
                    }
                ),
                400,
            )

        if verification_result is False:
            return (
                jsonify(
                    {
                        "message": "El DNI está registrado en el padrón, pero los datos ingresados son incorrectos."
                    }
                ),
                417,
            )

        return (
            jsonify({"message": "El individuo no está registrado en el Padrón."}),
            408,
        )

    return render_template('user_register/registro_votechain.html')


@vote_auth.route("/votechain/persona_info", methods=["GET", "POST"])
@google_login_required
@votechain_register_required
def persona_info(votechain_user, google_user):
    individuo_renaper = obtener_individuo_renaper(votechain_user)
    if request.method == "POST":
        response = post_nro_tramite(
            votechain_user,
            google_user,
            individuo_renaper,
            request.form.get("nro_tramite"),
        )

        if response == "success":
            return redirect(url_for("API-VOTE_AUTH.persona_info"))

        elif response == "invalid":
            api.message_info = f"Nro de trámite inválido. Cantidad de intentos restantes {votechain_user.tries}"
            return redirect(url_for("API-VOTE_AUTH.persona_info"))

        elif response == "no-tries":
            return redirect(url_for("API-VOTE_AUTH.exceeded_tries"))

    if individuo_renaper:
        api.message_info = votechain_user.tries
        if individuo_renaper.valid:
            validation_message = "Válido para votar."

        else:
            validation_message = "No válido para votar."

    return render_template(
        "user_register/persona_info_votechain.html",
        votechain_user=votechain_user,
        google_user=google_user,
        validation_message=validation_message,
        message=api.message_info,
    )


@vote_auth.route("/votechain/exceeded", methods=["GET"])
def exceeded_tries():
    session.clear()
    html = """
        <!DOCTYPE html>
        <html>

        <head>
            <title>Códigos excedidos</title>
        </head>

        <body>
            <h1>Has excedido la cantidad de intentos</h1>
            <a href="{{ url_for("API-GOOGLE_AUTH.index") }}"><button>Volver al inicio</button></a>
        </body>
        </html>
    """
    return render_template_string(html)