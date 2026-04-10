from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class TypeForfait(str, enum.Enum):
    prepaye = "prepaye"
    postpaye = "postpaye"
    hybride = "hybride"


class StatutAbonnement(str, enum.Enum):
    actif = "actif"
    suspendu = "suspendu"
    resilie = "resilie"


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False)
    prenom = Column(String(100), nullable=False)
    telephone = Column(String(20), unique=True, nullable=False)
    email = Column(String(150), unique=True, nullable=True)
    adresse = Column(Text, nullable=True)
    num_cni = Column(String(50), unique=True, nullable=True)

    # Champs télécom
    type_forfait = Column(Enum(TypeForfait), default=TypeForfait.prepaye)
    anciennete_mois = Column(Integer, default=0)
    statut_abonnement = Column(Enum(StatutAbonnement), default=StatutAbonnement.actif)
    revenu_estime = Column(Float, nullable=True)

    cree_le = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    usages = relationship("Usage", back_populates="client")
    historique_paiements = relationship("HistoriquePaiement", back_populates="client")
    demandes = relationship("Demande", back_populates="client")
    scores = relationship("ScoreRisque", back_populates="client")
    blacklist = relationship("Blacklist", back_populates="client", uselist=False)
