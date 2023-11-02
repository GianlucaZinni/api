from flask import redirect, url_for, session, request, jsonify
from functools import wraps
from votechain_api.stacks.api import api
from votechain_api.stacks.controller import controller
from layers.database.sqlalchemy.models import VotechainUser, GoogleUser

db_session = controller.db_session


def google_token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        authorization_header = request.headers.get("Authorization")
        if not (authorization_header and authorization_header.startswith("Bearer ")):
            return jsonify({"error": "Solicitud no válida. Sin Token."}), 400

        if authorization_header.split(" ")[1] != session.get("google_token"):
            return jsonify({"error": "Unauthorized. Token no válido"}), 401
        return f(*args, **kwargs)

    return decorated_function


def google_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "google_token" in session:
            user_data = api.google_key.get("userinfo").data

            if user_data.get("error"):
                return redirect(url_for("API-GOOGLE_AUTH.google_login"))

            google_user = (
                db_session.query(GoogleUser)
                .filter_by(id_google=user_data["id"])
                .first()
            )

            if not google_user:
                return redirect(url_for("API-GOOGLE_AUTH.google_login"))
            return f(google_user, *args, **kwargs)

        return redirect(url_for("API-GOOGLE_AUTH.google_login"))

    return decorated_function


def votechain_register_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_data = api.google_key.get("userinfo").data
        if not user_data.get("error"):
            votechain_user = (
                db_session.query(VotechainUser)
                .filter_by(id_google=user_data["id"])
                .first()
            )
            if not votechain_user:
                return redirect(url_for("API-VOTE_AUTH.register"))
            return f(votechain_user, *args, **kwargs)
        return redirect(url_for("API-GOOGLE_AUTH.google_login"))

    return decorated_function


def check_actually_register(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        
        if "google_token" in session:
            user_data = api.google_key.get("userinfo").data
            if not user_data.get("error"):
                # Verifica si el usuario ya está registrado en la base de datos
                user = (
                    db_session.query(VotechainUser).filter_by(id_google=user_data["id"]).first()
                )
                if user:
                    # Si el usuario ya está registrado, redirige a la página de userinfo
                    return redirect(url_for("API-VOTE_AUTH.person_info"))

                return redirect(url_for("API-VOTE_AUTH.register"))

        return f(*args, **kwargs)
            
    return decorated_function