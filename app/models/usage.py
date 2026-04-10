from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Usage(Base):
    __tablename__ = "usages"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    # Données de consommation télécom
    nb_appels = Column(Integer, default=0)
    duree_appels_min = Column(Float, default=0.0)
    volume_data_mo = Column(Float, default=0.0)
    nb_messages = Column(Integer, default=0)
    nb_recharges = Column(Integer, default=0)
    montant_recharge = Column(Float, default=0.0)

    # Période concernée
    mois = Column(Integer, nullable=False)
    annee = Column(Integer, nullable=False)

    cree_le = Column(DateTime(timezone=True), server_default=func.now())

    # Relation
    client = relationship("Client", back_populates="usages")
