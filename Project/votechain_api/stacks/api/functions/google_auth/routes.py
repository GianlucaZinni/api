from flask import redirect, url_for, session, Blueprint, jsonify
from votechain_api.stacks.api import api
from votechain_api.access import check_actually_register
from votechain_api.stacks.controller.functions.google_auth.index import save_google_user

google_auth = Blueprint("API-GOOGLE_AUTH", __name__)


@google_auth.route("/", methods=["GET", "POST"])
@check_actually_register
def index():
    return redirect(url_for("API-GOOGLE_AUTH.google_login"))


# Ruta para iniciar la autenticación de Google
@google_auth.route("/google/login", methods=["GET", "POST"])
@check_actually_register
def google_login():
    return api.google_key.authorize(
        callback=url_for("API-GOOGLE_AUTH.authorized", _external=True)
    )


# Ruta para recibir la respuesta de Google y autorizar al usuario
@google_auth.route("/google/login/authorized")
def authorized():
    response = api.google_key.authorized_response()
    if response is None or response.get("access_token") is None:
        return jsonify("Error al autorizar con Google"), 401

    # Almacena el token de acceso en la sesión del usuario
    session["google_token"] = response["access_token"]

    user_data = api.google_key.get("userinfo").data

    save_google_user(user_data)

    return redirect(url_for("API-VOTE_AUTH.register"))


# Ruta para cerrar sesión
@google_auth.route("/logout", methods=["GET", "POST"])
def logout():
    session.clear()
    return redirect(url_for("API-GOOGLE_AUTH.google_login"))
