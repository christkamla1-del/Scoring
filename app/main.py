from fastapi import FastAPI
from app.config import settings
from app.database import engine, Base
from app.models import (
    User,
    Client,
    Usage,
    HistoriquePaiement,
    Demande,
    ScoreRisque,
    Quotite,
    Blacklist,
)
from app.routers.auth import router as auth_router
from app.routers.scoring import router as scoring_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.include_router(auth_router)
app.include_router(scoring_router)


@app.get("/")
def root():
    return {"message": f"Bienvenue sur {settings.app_name}"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
