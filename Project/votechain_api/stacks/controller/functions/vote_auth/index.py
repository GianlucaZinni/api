from flask import Blueprint
from layers.database.sqlalchemy.models import VotechainUser
from votechain_api.stacks.controller import controller, sql_add, sql_delete

vote_auth = Blueprint("CONTROLLER-VOTE_AUTH", __name__)

db_session = controller.db_session


def check_already_register(google_user):
    return (
        db_session.query(VotechainUser)
        .filter_by(id_google=google_user.id_google)
        .first()
    )


def check_dni_already_exists(person_data):
    return db_session.query(VotechainUser).filter_by(DNI=person_data.get("dni")).first()


def insert_into_votechain(person_data, id_google):
    votechain_user = VotechainUser(
        DNI=person_data.get("dni"),
        id_google=id_google,
        nombre=person_data.get("nombre"),
        apellido=person_data.get("apellido"),
        telefono=person_data.get("telefono"),
    )
    sql_add(db_session, votechain_user)
    return db_session.commit()


def votechain_substact_tries(votechain_user):
    votechain_user.tries = votechain_user.tries - 1
    sql_add(db_session, votechain_user)
    return db_session.commit()


def post_nro_tramite(votechain_user, google_user, individuo_renaper, user_input):
    if votechain_user.tries > 1:
        if int(individuo_renaper.nro_tramite) == int(user_input):
            votechain_user.nro_tramite = user_input
            sql_add(db_session, votechain_user)
            db_session.commit()
            return "success"

        votechain_substact_tries(votechain_user)
        return "invalid"

    sql_delete(db_session, votechain_user)
    sql_delete(db_session, google_user)
    return "no-tries"
