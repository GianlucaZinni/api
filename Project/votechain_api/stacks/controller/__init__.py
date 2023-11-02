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


controller = ControllerStack()