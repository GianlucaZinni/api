from flask import (
    redirect,
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

    html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Registro en Votechain</title>
        </head>
        <body>
            <h1>Registro en Votechain</h1>
            <form method="POST">
                <label for="dni">DNI:</label>
                <input type="text" name="dni" required>
                <br>
                <label for="nombre">Nombre:</label>
                <input type="text" name="nombre" required>
                <br>
                <label for="apellido">Apellido:</label>
                <input type="text" name="apellido" required>
                <br>
                <label for="telefono">Teléfono:</label>
                <input type="text" name="telefono" required>
                <br>
                <button type="submit">Registrar</button>
            </form>
        </body>
        </html>
    """
    return render_template_string(html)


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

    html = """
        <!DOCTYPE html>
        <html>

        <head>
            <title>Información del usuario</title>
        </head>

        <body>
            <h1>Información del usuario</h1>
            <p for="DNI" value="{{ votechain_user.DNI }}">DNI: {{ votechain_user.DNI }} </p>
            <p for="nombre" value="{{ votechain_user.nombre }}">Nombre: {{ votechain_user.nombre }} </p>
            <p for="apellido" value="{{ votechain_user.apellido }}">Apellido: {{ votechain_user.apellido }} </p>
            <p for="email" value="{{ google_user.email }}">Correo Electrónico: {{ google_user.email }} </p>
            <p for="telefono" value="{{ votechain_user.telefono }}">Teléfono: {{ votechain_user.telefono }} </p>

            {% if votechain_user.nro_tramite %}
                <label for="nro_tramite">Número de Trámite: {{ votechain_user.nro_tramite }} </label>
                <br><br>
                <label> {{ validation_message }} </label>
                <br>
                <br>
                {% if validation_message == "Válido para votar." %}
                    <a href="{{ url_for("API-VOTE.validar_codigo") }}"><button>Ir a votar</button></a>
                {% endif %}
            {% else %}
                <form action="" method="POST">
                    <label for="nro_tramite">Número de Trámite: {{ nro_tramite }} {{ validation_message }} </label>
                    <input type="text" name="nro_tramite" id="nro_tramite">
                    <button type="submit">Enviar</button>
                </form>
                {% if message %}
                    <br>
                    <label value="{{ message }}"> Cantidad de intentos restantes: {{ message }} </label>
                {% endif %}
            {% endif %}
        </body>
        </html>
    """
    return render_template_string(
        html,
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