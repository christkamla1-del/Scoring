from fastapi import FastAPI
from app.config import settings
from app.database import engine, Base
from app.models import User, Client, Loan, Repayment, Blacklist

# Crée toutes les tables au démarrage
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/")
def root():
    return {"message": f"Bienvenue sur Test {settings.app_name}"}


@app.get("/health")
def health_check():
    return {"status": "ok"}
