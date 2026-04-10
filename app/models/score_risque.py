from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum


class CategorieRisque(str, enum.Enum):
    faible = "faible"
    moyen = "moyen"
    eleve = "eleve"
    critique = "critique"


class ScoreRisque(Base):
    __tablename__ = "scores_risque"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    demande_id = Column(Integer, ForeignKey("demandes.id"), nullable=False)

    # Résultat ML
    valeur_score = Column(Float, nullable=False)  # entre 0 et 1
    probabilite_defaut = Column(Float, nullable=False)  # entre 0 et 1
    categorie_risque = Column(Enum(CategorieRisque), nullable=False)

    # Explicabilité (features importantes)
    facteurs_principaux = Column(Text, nullable=True)  # JSON stocké en texte
    modele_utilise = Column(String(100), nullable=True)  # ex: "XGBoost v1.2"

    cree_le = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    client = relationship("Client", back_populates="scores")
    demande = relationship("Demande", back_populates="score")
    quotite = relationship("Quotite", back_populates="score", uselist=False)
