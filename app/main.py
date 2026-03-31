from fastapi import FastAPI
from app.config import settings

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

@app.get("/")
def root():
    return {"message": f"Bienvenue sur {settings.app_name}"}

@app.get("/health")
def health_check():
    return {"status": "ok"}