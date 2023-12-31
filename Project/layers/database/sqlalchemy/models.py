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
    tries = Column(Integer, nullable=False, default=3)
    
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
        return f"<Email Verification {self.DNI}, tiempo restante: {self.enabled}>"


# Modelo para la tabla Padrón en la base de datos RENAPER
class Padron(Base):
    __tablename__ = 'Padron'

    DNI = Column(BigInteger, primary_key=True)
    nombre = Column(String(255), nullable=False)
    apellido = Column(String(255), nullable=False)
    nro_tramite = Column(BigInteger, nullable=False)
    valid = Column(Boolean, nullable=False)
    
    def __repr__(self):
        return f"<Email Verification {self.DNI}, tiempo restante: {self.nro_tramite}, tries: {self.tries}>"
    

class CandidatosPresiVice(Base):
    __tablename__ = 'CandidatosPresiVice'

    candidatos_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre_presidente = Column(String(255), nullable=False)
    apellido_presidente = Column(String(255), nullable=False)
    nombre_vicepresidente = Column(String(255))
    apellido_vicepresidente = Column(String(255))
    foto_url = Column(String(255))

class PartidoPolitico(Base):
    __tablename__ = 'PartidoPolitico'

    partido_id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(255), nullable=False)
    lista = Column(String(10))
    siglas = Column(String(10))
    fundacion = Column(DateTime)
    logo_url = Column(String(255))
    candidatos_id = Column(Integer, ForeignKey('CandidatosPresiVice.candidatos_id'))

    candidatos = relationship('CandidatosPresiVice', backref='partidos')
