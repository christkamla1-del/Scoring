from sqlalchemy import Column, Integer, Float, String, Text, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class StatutDemande(str, enum.Enum):
    en_attente = "en_attente"
    approuvee = "approuvee"
    rejetee = "rejetee"
    annulee = "annulee"


class Demande(Base):
    __tablename__ = "demandes"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Téléphone demandé
    modele_telephone = Column(String(150), nullable=False)
    prix_telephone = Column(Float, nullable=False)

    statut = Column(Enum(StatutDemande), default=StatutDemande.en_attente)
    motif_rejet = Column(Text, nullable=True)

    cree_le = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    client = relationship("Client", back_populates="demandes")
    agent = relationship("User", back_populates="demandes")
    score = relationship("ScoreRisque", back_populates="demande", uselist=False)
    quotite = relationship("Quotite", back_populates="demande", uselist=False)
