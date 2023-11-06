from datetime import datetime
from flask import Blueprint
from layers.database.sqlalchemy.models import (
    Auditory,
    CandidatosPresiVice,
)
from votechain_api.stacks.controller import controller, sql_add

vote_auth = Blueprint("CONTROLLER-VOTE", __name__)

db_session = controller.db_session


def post_audit_vote(votechain_user):
    audit_user = db_session.query(Auditory).filter_by(DNI=votechain_user.DNI).first()
    audit_user.vote = True
    audit_user.vote_date = datetime.now()
    sql_add(db_session, votechain_user)


def get_candidatos():
    candidatos = db_session.query(CandidatosPresiVice).all()
    return candidatos


def get_partidos_politicos(candidato):
    return candidato.partidos

def check_if_valid(votechain_user):
    persona = db_session.query(Auditory).filter_by(DNI=votechain_user.DNI).first()
    print(persona)
    if persona:
        return True
    return False