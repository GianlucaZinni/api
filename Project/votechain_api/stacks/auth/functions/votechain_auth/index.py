from flask import redirect, url_for, session, render_template_string, Blueprint, flash
from votechain_api.stacks.auth.models import VotechainUsers, GoogleUsers
from votechain_api.stacks.auth import AuthStack
from votechain_api.stacks.auth.functions.votechain_auth.forms import RegistrationForm
from votechain_api.access import google_login_required, votechain_register_required

auth = AuthStack()

votechain_auth = Blueprint("Auth-votechain_auth", __name__)

db_session = auth.db_session


@google_login_required
@votechain_auth.route("/votechain/register", methods=["GET", "POST"])
def votechain_register():
    if "google_token" not in session:
        return redirect(url_for("Auth-google_auth.google_login"))

    user_data = auth.google.get("userinfo").data
    votechain_user = (
        db_session.query(VotechainUsers).filter_by(id=user_data["id"]).first()
    )

    if votechain_user:
        # Si el usuario ya está registrado, redirige a la página de userinfo
        return redirect(url_for("Auth-votechain_auth.user_info", _external=True))
    else:
        form = RegistrationForm()

        if form.validate_on_submit():
            # Verifica si el usuario ya existe en la base de datos
            persona = (
                db_session.query(VotechainUsers).filter_by(dni=form.dni.data).first()
            )
            if persona is None:
                email = (
                    db_session.query(VotechainUsers)
                    .filter_by(email=user_data["email"])
                    .first()
                )
                if email is None:
                    persona = VotechainUsers(
                        id=user_data["id"],
                        email=user_data["email"],
                        name=form.name.data,
                        surname=form.surname.data,
                        picture=user_data["picture"],
                        dni=form.dni.data,
                        telefono=form.telefono.data,
                    )
                    db_session.add(persona)
                    db_session.commit()
                    db_session.close()
                    return redirect(url_for("Auth-votechain_auth.user_info"))

            print(
                "Ya existe un usuario con ese DNI. Por favor, loguearse con el mail que ya registrado."
            )
            return redirect(url_for("Auth-votechain_auth.votechain_register"))
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
@google_login_required
def user_info():
    user_data = auth.google.get("userinfo").data
    google_user = (
        db_session.query(GoogleUsers).filter_by(google_id=user_data["id"]).first()
    )

    if not google_user:
        return redirect(url_for("Auth-google_auth.google_login"))

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
        <a href="{{ url_for("Vote-votacion.votar") }}"><button>Ir a votar</button></a>
        </html>
        """

        return render_template_string(response_html, user=user)
