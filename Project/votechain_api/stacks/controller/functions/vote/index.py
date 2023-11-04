from datetime import datetime
from flask import Blueprint
from layers.database.sqlalchemy.models import Auditory
from votechain_api.stacks.controller import controller, sql_add

vote_auth = Blueprint("CONTROLLER-VOTE", __name__)

db_session = controller.db_session


def post_vote(votechain_user):
    
    audit_user = db_session.query(Auditory).filter_by(DNI=votechain_user.DNI).first()
    audit_user.vote = True
    audit_user.vote_date = datetime.now()
    sql_add(db_session, votechain_user)

