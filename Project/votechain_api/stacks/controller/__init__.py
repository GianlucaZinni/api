from flask import Flask
from layers.database.sqlalchemy.index import SQLAlchemyHandler
from layers.resources import IntegratorResources


class ControllerStack:
    def __init__(self, app: Flask = None):
        # Access to the parameters resources
        resources = IntegratorResources()
        self.app = app

        # SQLAlchemy Handler
        self.sqlalchemy = SQLAlchemyHandler()
        self.db_session = self.sqlalchemy.connect("VOTECHAIN")
        self.db_session_renaper = self.sqlalchemy.connect("RENAPER")


def sql_add(db_session, register):
    db_session.add(register)
    db_session.commit()


def sql_delete(db_session, register):
    db_session.delete(register)
    db_session.commit()


controller = ControllerStack()
