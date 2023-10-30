from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from database import db_app

params = db_app.enviroment_variables

class SQLAlchemyHandler:
    
    def connect(self, database_name):
        engine = create_engine(f"{params['DB_CONFIG']['SQLALCHEMY']['DATABASE_URI']}{database_name}", echo=True)
        session_maker = sessionmaker(bind=engine)
        return session_maker()

    def close_db(session: Session):
        return session.close()