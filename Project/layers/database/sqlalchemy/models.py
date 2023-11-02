from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, BigInteger, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()

# Modelo para la tabla google_user
class GoogleUser(Base):
    __tablename__ = 'google_user'

    id_google = Column(String(255), primary_key=True)
    email = Column(String(255), nullable=False, unique=True)
    verified_email = Column(Boolean, nullable=False)
    picture = Column(String(255))

    # Relación con la tabla votechain_user (1 a 1)
    votechain_user = relationship("VotechainUser", uselist=False)

    def __repr__(self):
        return f"<Google User {self.email}>"


# Modelo para la tabla votechain_user
class VotechainUser(Base):
    __tablename__ = 'votechain_user'

    DNI = Column(BigInteger, primary_key=True)
    id_google = Column(Integer, ForeignKey('google_user.id_google'))
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    telefono = Column(String(15), nullable=False)
    nro_tramite = Column(BigInteger)
    
    def __repr__(self):
        return f"<Votechain User {self.nombre}, DNI: {self.DNI}>"

# Modelo para la tabla Email_Verification
class EmailVerification(Base):
    __tablename__ = 'Email_Verification'

    id_google = Column(Integer, ForeignKey('google_user.id_google'), primary_key=True)
    DNI = Column(Integer, ForeignKey('votechain_user.DNI'), primary_key=True)
    code = Column(Integer, nullable=False)
    tries = Column(Integer, nullable=False, default=3)
    expiration_time = Column(DateTime, nullable=False)
    
    def __repr__(self):
        return f"<Email Verification {self.code}, tiempo restante: {self.expiration_time}>"

# Modelo para la tabla Auditory
class Auditory(Base):
    __tablename__ = 'Auditory'

    DNI = Column(Integer, ForeignKey('votechain_user.DNI'), primary_key=True)
    enabled = Column(Boolean, default=False)
    enabled_date = Column(DateTime)
    vote = Column(Boolean, default=False)
    vote_date = Column(DateTime)

    
    def __repr__(self):
        return f"<Email Verification {self.code}, tiempo restante: {self.expiration_time}>"


# Modelo para la tabla Padrón en la base de datos RENAPER
class Padron(Base):
    __tablename__ = 'Padron'

    DNI = Column(BigInteger, primary_key=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    nro_tramite = Column(BigInteger, nullable=False)
    valid = Column(Boolean, nullable=False)