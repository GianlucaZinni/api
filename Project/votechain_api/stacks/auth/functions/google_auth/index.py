from flask import redirect, url_for, session, Blueprint
from votechain_api.stacks.auth.models import GoogleUsers
from votechain_api.stacks.auth import AuthStack

auth = AuthStack()

google_auth = Blueprint("GoogleAuth", __name__)

db_session = auth.db_session

# Ruta para iniciar la autenticación de Google
@google_auth.route("/google/login")
def google_login():
    return auth.google.authorize(
        callback=url_for("GoogleAuth.authorized", _external=True)
    )


# Ruta para recibir la respuesta de Google y autorizar al usuario
@google_auth.route("/google/login/authorized")
def authorized():
    response = auth.google.authorized_response()
    if response is None or response.get("access_token") is None:
        return "Error al autorizar con Google"

    # Almacena el token de acceso en la sesión del usuario
    session["google_token"] = response["access_token"]

    user_info = auth.google.get("userinfo")
    user_data = user_info.data
    
    # Verifica si el usuario ya existe en la base de datos
    user = db_session.query(GoogleUsers).filter_by(email=user_data["email"]).first()
    print(user)
    if user is None:
        user = GoogleUsers(
            google_id=user_data.get("id"),
            email=user_data.get("email"),
            verified_email=user_data.get("verified_email"),
            name=user_data.get("given_name", ""),
            surname=user_data.get("family_name", ""),
            picture=user_data.get("picture", ""),
        )
        db_session.add(user)
        db_session.commit()
    return redirect(url_for("VotechainAuth.votechain_register"))


# Ruta para cerrar sesión
@google_auth.route("/logout")
def logout():
    session.pop("google_token", None)
    return redirect(url_for("index"))


@google_auth.route("/")
def index():
    return "Hola locura! -- <a href='/google/login'><button>Login</button></a>"
