from flask import redirect, url_for, render_template_string, Blueprint, jsonify, request, session
from layers.database.sqlalchemy.models import VotechainUser
from votechain_api.stacks.api import api
from votechain_api.stacks.controller import controller
from votechain_api.access import (
    google_login_required,
    google_token_required,
    votechain_register_required,
)
from votechain_api.stacks.controller.functions.renaper.index import (
    verificar_en_padron,
    verificar_nro_tramite,
)

vote_auth = Blueprint("API-VOTE_AUTH", __name__)

db_session = controller.db_session

@vote_auth.route("/votechain/register", methods=["GET", "POST"])
@google_login_required
def register(google_user):
    if (
        db_session.query(VotechainUser)
        .filter_by(id_google=google_user.id_google)
        .first()
    ):
        return redirect(url_for("API-VOTE_AUTH.person_info"))

    if request.method == "POST":
        persona_data = request.form

        if not persona_data:
            return jsonify({"error": "Solicitud no válida"}), 400

        dni = persona_data.get("dni")

        verification_result = verificar_en_padron(persona_data)

        if verification_result:
            # Verifica que no exista un individuo ya registrado con el mismo id_google
            if (
                db_session.query(VotechainUser)
                .filter_by(id_google=google_user.id_google)
                .first()
            ):
                return jsonify({"message": "Ya estás registrado."}), 200

            # Verifica si el usuario ya existe en la base de datos
            if db_session.query(VotechainUser).filter_by(DNI=dni).first():
                return (
                    jsonify(
                        {
                            "message": "El DNI ya está registrado a una cuenta de email distinta."
                        }
                    ),
                    400,
                )

            votechain_user = VotechainUser(
                DNI=dni,
                id_google=google_user.id_google,
                nombre=persona_data.get("nombre"),
                apellido=persona_data.get("apellido"),
                telefono=persona_data.get("telefono"),
            )
            db_session.add(votechain_user)
            db_session.commit()
            db_session.close()
            return redirect(url_for("API-VOTE_AUTH.person_info"))

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


@vote_auth.route("/votechain/person_info", methods=["GET", "POST"])
@google_login_required
@votechain_register_required
def person_info(votechain_user, google_user):
    valid_nro_tramite, nro_tramite = verificar_nro_tramite(votechain_user)
    if api.count_nro_tramite <= 0:
        db_session.delete(votechain_user)
        db_session.delete(google_user)
        db_session.commit()
        db_session.close()
        api.count_nro_tramite = 4
        api.message = ""
        return redirect(url_for("API-GOOGLE_AUTH.logout"))
    
    validation_message = ""
    if not votechain_user.nro_tramite:
        if request.method == "POST":
            if str(request.form["nro_tramite"]) == str(nro_tramite):
                votechain_user.nro_tramite = request.form["nro_tramite"]
                db_session.add(votechain_user)
                db_session.commit()
                db_session.close()
                return redirect(url_for("API-VOTE_AUTH.person_info"))
            api.count_nro_tramite -= 1
            api.message = f"Nro de trámite inválido. Cantidad de intentos restantes {controller.count_nro_tramite}"
            return redirect(url_for("API-VOTE_AUTH.person_info"))

    else:
        if valid_nro_tramite:
            validation_message = "Válido para votar."
            api.message = ""

        else:
            validation_message = "No válido para votar."
            api.message = ""

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
                <label for="nro_tramite">Número de Trámite: {{ nro_tramite }} {{ validation_message }} </label>
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
            {% endif %}
                        
            {% if message %}
                <br>
                <label value="{{ message }}"> {{ message }} </label>
            {% endif %}
        
        </body>
        </html>
    """
    return render_template_string(
        html,
        votechain_user=votechain_user,
        google_user=google_user,
        validation_message=validation_message,
        message=api.message,
    )
