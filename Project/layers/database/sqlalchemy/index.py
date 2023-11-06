from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import os

class SQLAlchemyHandler:
    
    def connect(self, database_name):
        engine = create_engine(f"{os.getenv('DATABASE_URI')}/{database_name}")
        session_maker = sessionmaker(bind=engine)
        return session_maker()

    def close_db(session: Session):
        return session.close()