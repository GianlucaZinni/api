from flask import redirect, url_for, session
from functools import wraps
from votechain_api.stacks.auth import AuthStack
from votechain_api.stacks.auth.models import VotechainUsers

auth = AuthStack()
db_session = auth.db_session


def google_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "google_token" in session:
            return f(*args, **kwargs)
        else:
            # Redirige al usuario a la página de inicio de sesión de Google.
            return redirect(url_for("Auth-google_auth.google_login"))

    return decorated_function


def votechain_register_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verifica si el usuario está autenticado en Votechain
        if "google_token" not in session:
            return redirect(url_for("Auth-google_auth.google_login"))

        user_info = auth.google.get("userinfo")
        user_data = user_info.data

        # Verifica si el usuario ya existe en la base de datos de Votechain
        user = db_session.query(VotechainUsers).filter_by(id=user_data["id"]).first()

        if user:
            # Si el usuario ya está registrado, permite el acceso a la función original.
            return f(*args, **kwargs)
        else:
            # Si el usuario no está registrado, redirige a la página de registro de Votechain.
            return redirect(url_for("Auth-votechain_auth.votechain_register"))

    return decorated_function
