from votechain_api.stacks.controller import controller
from sqlalchemy import exists, and_
from layers.database.sqlalchemy.models import Padron

db_session_renaper = controller.db_session_renaper


def verificar_nro_tramite(votechain_user: dict) -> bool:
    individuo = (
        db_session_renaper.query(Padron).filter_by(DNI=votechain_user.DNI).first()
    )
    return individuo.valid, individuo.nro_tramite


def verificar_en_padron(persona_data: dict) -> bool:
    individuo = (
        db_session_renaper.query(Padron).filter_by(DNI=persona_data.get("dni")).first()
    )
    if individuo:
        if db_session_renaper.query(
            exists().where(
                and_(
                    Padron.DNI == individuo.DNI,
                    Padron.nombre == persona_data.get("nombre"),
                    Padron.apellido == persona_data.get("apellido"),
                )
            )
        ).scalar():
            return True
        return False
    return
