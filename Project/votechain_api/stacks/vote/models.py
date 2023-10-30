from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime

Base = declarative_base()

class EmailVerification(Base):
    __tablename__ = "email_verification"
    code = Column(String(8),  primary_key=True, unique=True, nullable=False)
    expiration_time = Column(DateTime, nullable=False)
    google_id = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"<Email Verification {self.code}, tiempo restante: {self.expiration_time}>"

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
