from flask import redirect, url_for, session, Blueprint

vote = Blueprint("VotechainVote", __name__)

# db = auth_app.sqlalchemy.db

# class GoogleUsers(db.Model):
#     __tablename__ = "google_users"
#     google_id = db.Column(db.String(255), primary_key=True, unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     verified_email = db.Column(db.Boolean(), nullable=False)
#     name = db.Column(db.String(120))
#     surname = db.Column(db.String(120))
#     picture = db.Column(db.String(120))


# with auth_app.app.app_context():
#     db.create_all()


# # Ruta para iniciar la autenticación de Google
# @vote.route("/google/login")
# def google_login():
#     return auth_app.google.authorize(callback=url_for("GoogleAuth.authorized", _external=True))


# # Ruta para recibir la respuesta de Google y autorizar al usuario
# @vote.route("/google/login/authorized")
# def authorized():
#     response = auth_app.google.authorized_response()
#     if response is None or response.get("access_token") is None:
#         return "Error al autorizar con Google"

#     # Almacena el token de acceso en la sesión del usuario
#     session["google_token"] = response["access_token"]

#     user_info = auth_app.google.get("userinfo")
#     user_data = user_info.data
#     # Verifica si el usuario ya existe en la base de datos
#     user = GoogleUsers.query.filter_by(email=user_data["email"]).first()
#     if user is None:
#         user = GoogleUsers(
#             google_id=user_data["id"],
#             email=user_data["email"],
#             verified_email=user_data["verified_email"],
#             name=user_data["given_name"],
#             surname=user_data["family_name"],
#             picture=user_data["picture"],
#         )
#         db.session.add(user)
#         db.session.commit()

#     return redirect(url_for("VotechainAuth.votechain_register"))


# # Ruta para cerrar sesión
# @vote.route("/logout")
# def logout():
#     session.pop("google_token", None)
#     return redirect(url_for("index"))


@vote.route("/")
def index():
    return "LCDSTM"
