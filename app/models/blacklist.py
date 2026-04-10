from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base


class Blacklist(Base):
    __tablename__ = "blacklist"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.id"), unique=True, nullable=False)
    agent_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    motif = Column(Text, nullable=False)
    est_actif = Column(Boolean, default=True)
    cree_le = Column(DateTime(timezone=True), server_default=func.now())

    # Relations
    client = relationship("Client", back_populates="blacklist")
    agent = relationship("User", back_populates="blacklists")
