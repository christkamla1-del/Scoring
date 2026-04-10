from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum, Text, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class StatutValidation(str, enum.Enum):
    proposee = "proposee"
    validee = "validee"
    ajustee = "ajustee"
    rejetee = "rejetee"


class Quotite(Base):
    __tablename__ = "quotites"

    id = Column(Integer, primary_key=True, index=True)
    demande_id = Column(Integer, ForeignKey("demandes.id"), nullable=False)
    score_id = Column(Integer, ForeignKey("scores_risque.id"), nullable=False)
    valideur_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Calcul automatique ML
    quotite_proposee = Column(Float, nullable=False)  # % du prix financé
    montant_propose = Column(Float, nullable=False)  # montant en FCFA

    # Ajustement manuel admin
    quotite_finale = Column(Float, nullable=True)
    montant_final = Column(Float, nullable=True)
    ajustement_manuel = Column(Boolean, default=False)
    motif_ajustement = Column(Text, nullable=True)

    statut = Column(Enum(StatutValidation), default=StatutValidation.proposee)
    valide_le = Column(DateTime(timezone=True), nullable=True)
    cree_le = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    demande = relationship("Demande", back_populates="quotite")
    score = relationship("ScoreRisque", back_populates="quotite")
    valideur = relationship("User", back_populates="quotites")
