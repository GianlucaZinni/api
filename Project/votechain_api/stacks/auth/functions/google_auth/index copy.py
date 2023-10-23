from flask import Flask, redirect, url_for, session, request, render_template_string
from flask_oauthlib.client import OAuth
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm
from functools import wraps

app = Flask(__name__)

# Configuración de Flask
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:42886236@localhost/GoogleAUTH_DB"
app.secret_key = "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"
db = SQLAlchemy(app)

# Configuración de Google OAuth
app.config[
    "GOOGLE_ID"
] = "763831980100-jla6gkspnss9vqkc13kblqe9mjht0ib1.apps.googleusercontent.com"
app.config["GOOGLE_SECRET"] = "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"
app.config["GOOGLE_REDIRECT_URI"] = "/google/login/authorized"

oauth = OAuth(app)

google = oauth.remote_app(
    "google",
    consumer_key=app.config["GOOGLE_ID"],
    consumer_secret=app.config["GOOGLE_SECRET"],
    request_token_params={
        "scope": "email profile",  # Solicitar acceso al correo electrónico y al perfil del usuario
    },
    base_url="https://www.googleapis.com/oauth2/v1/",
    request_token_url=None,
    access_token_method="POST",
    access_token_url="https://accounts.google.com/o/oauth2/token",
    authorize_url="https://accounts.google.com/o/oauth2/auth",
)


def google_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "google_token" in session:
            return f(*args, **kwargs)
        else:
            # Redirige al usuario a la página de inicio de sesión de Google.
            return redirect(url_for("google_login"))

    return decorated_function


def votechain_register_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verifica si el usuario está autenticado en Votechain
        if "google_token" not in session:
            return redirect(url_for("google_login"))

        user_info = google.get("userinfo")
        user_data = user_info.data

        # Verifica si el usuario ya existe en la base de datos de Votechain
        user = VotechainUser.query.filter_by(id=user_data["id"]).first()

        if user:
            # Si el usuario ya está registrado, permite el acceso a la función original.
            return f(*args, **kwargs)
        else:
            # Si el usuario no está registrado, redirige a la página de registro de Votechain.
            return redirect(url_for("votechain_register"))

    return decorated_function


# El tokengetter en Flask-OAuthlib se define en el objeto 'google'
@google.tokengetter
def get_google_oauth_token():
    return session.get("google_token")


class GoogleUser(db.Model):
    __tablename__ = "google_users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    google_id = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    verified_email = db.Column(db.Boolean(), nullable=False)
    name = db.Column(db.String(120))
    surname = db.Column(db.String(120))
    picture = db.Column(db.String(120))


class VotechainUser(db.Model):
    id = db.Column(db.String(255), primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120))
    surname = db.Column(db.String(120))
    dni = db.Column(db.Integer, unique=True, nullable=False)
    telefono = db.Column(db.String(20), unique=True, nullable=False)
    picture = db.Column(db.String(120))
    public_key = db.Column(db.String(256), unique=True, nullable=False)
    private_key = db.Column(db.String(256), unique=True, nullable=False)


with app.app_context():
    db.create_all()


# Ruta para iniciar la autenticación de Google
@app.route("/google/login")
def google_login():
    return google.authorize(callback=url_for("authorized", _external=True))


# Ruta para recibir la respuesta de Google y autorizar al usuario
@app.route("/google/login/authorized")
def authorized():
    response = google.authorized_response()
    if response is None or response.get("access_token") is None:
        return "Error al autorizar con Google"

    # Almacena el token de acceso en la sesión del usuario
    session["google_token"] = response["access_token"]

    user_info = google.get("userinfo")
    user_data = user_info.data
    # Verifica si el usuario ya existe en la base de datos
    user = GoogleUser.query.filter_by(email=user_data["email"]).first()
    if user is None:
        user = GoogleUser(
            google_id=user_data["id"],
            email=user_data["email"],
            verified_email=user_data["verified_email"],
            name=user_data["given_name"],
            surname=user_data["family_name"],
            picture=user_data["picture"],
        )
        db.session.add(user)
        db.session.commit()

    return redirect(url_for("votechain_register"))


@google_login_required
@app.route("/votechain/register", methods=["GET", "POST"])
def votechain_register():
    if "google_token" not in session:
        return redirect(url_for("google_login"))

    user_info = google.get("userinfo")
    user_data = user_info.data

    # Verifica si el usuario ya existe en la base de datos de Votechain
    user = VotechainUser.query.filter_by(id=user_data["id"]).first()

    if user:
        # Si el usuario ya está registrado, redirige a la página de userinfo
        return redirect(url_for("user_info"))

    form = RegistrationForm()

    if form.validate_on_submit():
        # Verifica si el usuario ya existe en la base de datos
        user = VotechainUser.query.filter_by(id=user_data["id"]).first()
        if user is None:
            user = VotechainUser(
                id=user_data["id"],
                email=user_data["email"],
                name=form.name.data,
                surname=form.surname.data,
                picture=user_data["picture"],
                dni=form.dni.data,
                telefono=form.telefono.data,
                public_key="^$%^*#$%@#$R%@#$",
                private_key="%^&$%^@#$@#$@$@",
            )
            db.session.add(user)
            db.session.commit()

        return url_for("user_info", _external=True)

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


@app.route("/votechain/user_info", methods=["GET"])
@google_login_required  # Requiere autenticación de Google
@votechain_register_required  # Requiere autenticación de Votechain
def user_info():
    user_info = google.get("userinfo")
    user_data = user_info.data
    user = VotechainUser.query.filter_by(id=user_data["id"]).first()

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


# Ruta para cerrar sesión
@app.route("/logout")
def logout():
    session.pop("google_token", None)
    return redirect(url_for("index"))


@app.route("/")
def index():
    return "Hola locura! -> <a href='/google/login'><button>Login</button></a>"


if __name__ == "__main__":
    app.run(debug=True, port=5001)
