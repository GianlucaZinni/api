from flask import (
    redirect,
    render_template,
    url_for,
    Blueprint,
    request,
    session,
    flash
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
        try:
            dni = int(persona_data.get("dni", "").strip())
        except ValueError:
            flash("DNI debe ser un número.", "error")
            return redirect(url_for("API-VOTE_AUTH.register"))

        nombre = persona_data.get("nombre", "").strip()
        apellido = persona_data.get("apellido", "").strip()
        telefono = persona_data.get("telefono", "").strip()

        if not nombre or not apellido:
            flash("Nombre y apellido son obligatorios.", "error")
            return redirect(url_for("API-VOTE_AUTH.register"))
        
        if not persona_data:
            flash("No has enviado informacion", "error")
            return redirect(url_for("API-VOTE_AUTH.register"))

        verification_result = verificar_en_padron(persona_data)

        if verification_result:
            if not check_dni_already_exists(persona_data):
                insert_into_votechain(persona_data, google_user.id_google)
                return redirect(url_for("API-VOTE_AUTH.persona_info"))
            flash("El DNI ya está registrado a una cuenta de email distinta.", "error")
            return redirect(url_for("API-VOTE_AUTH.register"))


        if verification_result is False:
            flash("El DNI está registrado en el padrón, pero los datos ingresados son incorrectos.", "error")
            return redirect(url_for("API-VOTE_AUTH.register"))

        flash("El individuo no está registrado en el Padrón.", "error")
        return redirect(url_for("API-VOTE_AUTH.register"))
    
    return render_template('user_register/registro_votechain.html')

@vote_auth.route("/votechain/persona_info", methods=["GET", "POST"])
@google_login_required
@votechain_register_required
def persona_info(votechain_user, google_user):
    individuo_renaper = obtener_individuo_renaper(votechain_user)
    validation_message = None

    if request.method == "POST":
        nro_tramite_str = request.form.get("nro_tramite", "").strip()
        
        # Verificar que el número de trámite sea un entero
        try:
            nro_tramite = int(nro_tramite_str)
        except ValueError:
            flash("El número de trámite debe ser un número entero.", "error")
            return redirect(url_for("API-VOTE_AUTH.persona_info"))
        
        response = post_nro_tramite(
            votechain_user,
            google_user,
            individuo_renaper,
            request.form.get("nro_tramite"),
        )
        if response == "success":
            flash('Número de trámite aceptado con éxito.', 'success')
            return redirect(url_for("API-VOTE_AUTH.persona_info"))
        elif response == "invalid":
            flash(f'Nro de trámite inválido. Cantidad de intentos restantes {votechain_user.tries}', 'error')
            return redirect(url_for("API-VOTE_AUTH.persona_info"))
        elif response == "no-tries":
            flash('Has excedido el número máximo de intentos.', 'error')
            return redirect(url_for("API-VOTE_AUTH.exceeded_tries"))

    if individuo_renaper:
        api.message_info = votechain_user.tries
        if individuo_renaper.valid and votechain_user.nro_tramite:
            validation_message = "Válido para votar."
        elif not individuo_renaper.valid and votechain_user.nro_tramite:
            validation_message = "No válido para votar."
        else:
            validation_message = ""

    return render_template(
        "user_register/persona_info_votechain.html",
        votechain_user=votechain_user,
        google_user=google_user,
        validation_message=validation_message,
        message=api.message_info,
    )

@vote_auth.route("/votechain/exceeded", methods=["GET"])
def exceeded_tries():
    session.clear()
    return render_template("user_register/codigos_excedidos.html")