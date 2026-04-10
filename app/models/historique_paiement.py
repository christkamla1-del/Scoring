from sqlalchemy import Column, Integer, Float, Date, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class StatutPaiement(str, enum.Enum):
    paye = "paye"
    en_retard = "en_retard"
    impaye = "impaye"


class HistoriquePaiement(Base):
    __tablename__ = "historique_paiements"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    montant_du = Column(Float, nullable=False)
    montant_paye = Column(Float, default=0.0)
    nb_retards = Column(Integer, default=0)
    nb_impayes = Column(Integer, default=0)
    jours_retard = Column(Integer, default=0)
    statut = Column(Enum(StatutPaiement), default=StatutPaiement.paye)
    date_echeance = Column(Date, nullable=False)
    date_paiement = Column(Date, nullable=True)
    est_regularise = Column(Boolean, default=False)

    cree_le = Column(DateTime(timezone=True), server_default=func.now())

    # Relation
    client = relationship("Client", back_populates="historique_paiements")
