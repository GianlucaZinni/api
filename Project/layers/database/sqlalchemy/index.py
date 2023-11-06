from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os
from layers.database import db_app

params = db_app.enviroment_variables


class SQLAlchemyHandler:
    def connect(self, database_name):
        engine = create_engine(f"{os.getenv('DATABASE_URI')}/{database_name}")
        session_maker = sessionmaker(bind=engine)
        return session_maker()

    def close_db(session: Session):
        return session.close()
