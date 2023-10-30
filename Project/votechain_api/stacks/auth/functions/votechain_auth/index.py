from flask import redirect, url_for, session, render_template_string, Blueprint
from functools import wraps
from votechain_api.stacks.auth.models import VotechainUsers
from votechain_api.stacks.auth import AuthStack
from votechain_api.stacks.auth.functions.votechain_auth.forms import RegistrationForm

auth = AuthStack()

votechain_auth = Blueprint("VotechainAuth", __name__)

db_session = auth.db_session

def google_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "google_token" in session:
            return f(*args, **kwargs)
        else:
            # Redirige al usuario a la página de inicio de sesión de Google.
            return redirect(url_for("GoogleAuth.google_login"))

    return decorated_function


def votechain_register_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verifica si el usuario está autenticado en Votechain
        if "google_token" not in session:
            return redirect(url_for("GoogleAuth.google_login"))

        user_info = auth.google.get("userinfo")
        user_data = user_info.data

        # Verifica si el usuario ya existe en la base de datos de Votechain
        user = db_session.query(VotechainUsers).filter_by(id=user_data["id"]).first()

        if user:
            # Si el usuario ya está registrado, permite el acceso a la función original.
            return f(*args, **kwargs)
        else:
            # Si el usuario no está registrado, redirige a la página de registro de Votechain.
            return redirect(url_for("VotechainAuth.votechain_register"))

    return decorated_function


@google_login_required
@votechain_auth.route("/votechain/register", methods=["GET", "POST"])
def votechain_register():
    if "google_token" not in session:
        return redirect(url_for("GoogleAuth.google_login"))

    user_info = auth.google.get("userinfo")
    user_data = user_info.data

    # Verifica si el usuario ya existe en la base de datos de Votechain
    user = db_session.query(VotechainUsers).filter_by(id=user_data["id"]).first()

    if user:
        # Si el usuario ya está registrado, redirige a la página de userinfo
        return redirect(url_for("VotechainAuth.user_info"))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Verifica si el usuario ya existe en la base de datos
        user = db_session.query(VotechainUsers).filter_by(id=user_data["id"]).first()
        if user is None:
            user = VotechainUsers(
                id=user_data["id"],
                email=user_data["email"],
                name=form.name.data,
                surname=form.surname.data,
                picture=user_data["picture"],
                dni=form.dni.data,
                telefono=form.telefono.data,
            )
            db_session.add(user)
            db_session.commit()
            
        return redirect(url_for("VotechainAuth.user_info"))

    # Crea una cadena de texto HTML para el formulario
    form_html = """
    <form method="POST">
        {{ form.hidden_tag() }}
        <label for="name">Nombre:</label>
        <input type="text" name="name" id="name"><br><br>
        <label for="surname">Apellido:</label>
        <input type="text" name="surname" id="surname"><br><br>
        <label for="dni">DNI:</label>
        <input type="text" name="dni" id="dni"><br><br>
        <label for="telefono">Teléfono:</label>
        <input type="text" name="telefono" id="telefono" value="{{ form.telefono.data }}"><br><br>
        <input type="submit" value="Registrar">
    </form>
    """

    return render_template_string(form_html, form=form)


@votechain_auth.route("/votechain/user_info", methods=["GET"])
@google_login_required  # Requiere autenticación de Google
@votechain_register_required  # Requiere autenticación de Votechain
def user_info():
    user_info = auth.google.get("userinfo")
    user_data = user_info.data
    user = db_session.query(VotechainUsers).filter_by(id=user_data["id"]).first()

    if user:
        # Crea una cadena de texto HTML de respuesta
        response_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Información del usuario</title>
        </head>
        <body>
            <h1>Información del usuario</h1>
            <p for="Nombre" value="{{ user.name }}">Nombre: {{ user.name }} </p>
            <p for="Apellido" value="{{ user.surname }}">Apellido: {{ user.surname }} </p>
            <p for="Correo Electronico" value="{{ user.email }}">Correo Electronico: {{ user.email }} </p>
            <p for="DNI" value="{{ user.dni }}">DNI: {{ user.dni }} </p>
            <p for="Teléfono" value="{{ user.telefono }}">Teléfono: {{ user.telefono }} </p>
        </body>
        <a href='/auth'><button>Ir a votar</button></a>
        </html>
        """

        return render_template_string(response_html, user=user)
