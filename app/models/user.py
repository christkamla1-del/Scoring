from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class RoleEnum(str, enum.Enum):
    admin = "admin"
    agent = "agent"
    superviseur = "superviseur"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    mot_de_passe = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.agent)
    est_actif = Column(Boolean, default=True)
    cree_le = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    demandes = relationship("Demande", back_populates="agent")
    blacklists = relationship("Blacklist", back_populates="agent")
    quotites = relationship("Quotite", back_populates="valideur")
