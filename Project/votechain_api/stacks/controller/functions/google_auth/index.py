from votechain_api.stacks.controller import controller, sql_add
from layers.database.sqlalchemy.models import GoogleUser

db_session = controller.db_session

def save_google_user(user_data):
    # Verifica si el usuario ya existe en la base de datos
    user = db_session.query(GoogleUser).filter_by(email=user_data["email"]).first()

    if user is None:
        user = GoogleUser(
            id_google=user_data.get("id"),
            email=user_data.get("email"),
            verified_email=user_data.get("verified_email"),
            picture=user_data.get("picture", ""),
        )
        sql_add(db_session, user)
        db_session.commit()