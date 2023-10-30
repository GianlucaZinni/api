from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

Base = declarative_base()

class GoogleUsers(Base):
    __tablename__ = "google_users"
    google_id = Column(String(255), primary_key=True, unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    verified_email = Column(Boolean(), nullable=False)
    name = Column(String(120))
    surname = Column(String(120))
    picture = Column(String(120))
    
    def __repr__(self):
        return f"<Google User {self.email}>"

class VotechainUsers(Base):
    __tablename__ = "votechain_users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(120), unique=True, nullable=False)
    name = Column(String(120))
    surname = Column(String(120))
    dni = Column(Integer, unique=True, nullable=False)
    telefono = Column(String(20), unique=True, nullable=False)
    picture = Column(String(120))
    
    def __repr__(self):
        return f"<Votechain User {self.email}>"
