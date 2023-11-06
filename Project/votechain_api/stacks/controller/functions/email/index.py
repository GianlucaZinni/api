import random
from datetime import datetime, timedelta
from votechain_api.stacks.controller import controller, sql_add, sql_delete
from layers.database.sqlalchemy.models import EmailVerification, Auditory
from layers.email.index import enviar_correo

db_session = controller.db_session


def clean_expired_verification_codes():
    expiration_limit = datetime.now().replace(microsecond=0)
    expired_codes = (
        db_session.query(EmailVerification)
        .filter(EmailVerification.expiration_time <= expiration_limit)
        .all()
    )
    print(expiration_limit)
    print(expired_codes)
    for code in expired_codes:
        db_session.delete(code)

    db_session.commit()


def generate_eightdigits_code(DNI, id_google):
    new_code = "".join([str(random.randint(0, 9)) for _ in range(8)])
    existing_code = db_session.query(EmailVerification).filter_by(code=new_code).first()
    if existing_code:
        return generate_eightdigits_code(DNI, id_google)

    expiration_time = datetime.now() + timedelta(seconds=300)
    code = EmailVerification(
        code=new_code,
        expiration_time=expiration_time,
        id_google=id_google,
        DNI=DNI,
    )
    sql_add(db_session, code)
    return code


def check_exists_code(votechain_user, google_user):
    return (
        db_session.query(EmailVerification)
        .filter_by(id_google=google_user.id_google, DNI=votechain_user.DNI)
        .first()
    )


def get_email_code(votechain_user, google_user):
    code = check_exists_code(votechain_user, google_user)
    if not code:
        verification_code = generate_eightdigits_code(
            votechain_user.DNI, google_user.id_google
        )
        if isinstance(verification_code, EmailVerification):
            enviar_correo(
                votechain_user,
                google_user,
                verification_code.code,
            )
    return code


def post_email_code(votechain_user, google_user, code, user_input):
    if code.tries > 1:
        if int(code.code) == int(user_input):
            auditory = Auditory(
                DNI=votechain_user.DNI,
                enabled=True,
                enabled_date=datetime.now(),
            )
            sql_add(db_session, auditory)
            sql_delete(db_session, code)

            return "success"

        code.tries = code.tries - 1
        sql_add(db_session, code)
        return "invalid"

    sql_delete(db_session, code)
    sql_delete(db_session, votechain_user)
    sql_delete(db_session, google_user)
    return "no-tries"
