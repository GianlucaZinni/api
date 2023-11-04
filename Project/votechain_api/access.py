from flask import redirect, url_for, session
from functools import wraps
from votechain_api.stacks.api import api
from votechain_api.stacks.controller import controller
from layers.database.sqlalchemy.models import VotechainUser, GoogleUser, Auditory

db_session = controller.db_session


def verify_google_token(model, first_redirect, second_redirect, third_redirect):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "google_token" in session:
                user_data = api.google_key.get("userinfo").data
                if not user_data.get("error"):
                    # Verifica si el usuario ya está registrado en la base de datos
                    user = (
                        db_session.query(model)
                        .filter_by(id_google=user_data.get("id"))
                        .first()
                    )
                    if user:
                        return f(user, *args, **kwargs)

                    return redirect(url_for(first_redirect))

                return redirect(url_for(second_redirect))

            return redirect(url_for(third_redirect))

        return decorated_function

    return decorator


google_login_required = verify_google_token(
    GoogleUser,
    "API-GOOGLE_AUTH.google_login",
    "API-GOOGLE_AUTH.google_login",
    "API-GOOGLE_AUTH.google_login",
)

votechain_register_required = verify_google_token(
    VotechainUser,
    "API-VOTE_AUTH.register",
    "API-GOOGLE_AUTH.google_login",
    "API-GOOGLE_AUTH.google_login",
)

def verify_actually(
    model1,
    model2,
    first_redirect,
    second_redirect,
    third_redirect,
    fourth_redirect=None,
    fifth_redirect=None
):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if "google_token" in session:
                user_data = api.google_key.get("userinfo").data
                if not user_data.get("error"):
                    # Verifica si el usuario ya está registrado en la base de datos
                    user = (
                        db_session.query(model1)
                        .filter_by(id_google=user_data.get("id"))
                        .first()
                    )
                    if user:
                        if model2:
                            audit_user = (
                                db_session.query(model2).filter_by(DNI=user.DNI).first()
                            )
                            if audit_user:
                                
                                vote_user = (
                                    db_session.query(model2).filter_by(DNI=user.DNI, vote=True).first()
                                )
                                if not vote_user:
                                    return f(*args, **kwargs)
                                
                                if vote_user:
                                    return redirect(url_for(fifth_redirect))
                                    
                                return redirect(url_for(fourth_redirect))
                        
                            return f(*args, **kwargs)

                        return redirect(url_for(third_redirect))

                    return redirect(url_for(second_redirect))

                return redirect(url_for(first_redirect))

            return f(*args, **kwargs)

        return decorated_function

    return decorator


verify_actually_register = verify_actually(
    VotechainUser,
    None,
    "API-GOOGLE_AUTH.google_login",
    "API-VOTE_AUTH.register",
    "API-VOTE_AUTH.persona_info",
)

verify_actually_audit = verify_actually(
    VotechainUser,
    Auditory,
    "API-GOOGLE_AUTH.google_login",
    "API-VOTE_AUTH.register",
    "API-VOTE_AUTH.persona_info",
    "API-VOTE.candidatos",
    "API-VOTE.votado"
)

verify_actually_vote = verify_actually(
    VotechainUser,
    Auditory,
    "API-GOOGLE_AUTH.google_login",
    "API-VOTE_AUTH.register",
    "API-VOTE_AUTH.persona_info",
    "API-VOTE.candidatos",
    "API-VOTE.votado"
)