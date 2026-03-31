from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_host: str
    db_port: int = 3306
    db_name: str
    db_user: str
    db_password: str

    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60

    app_name: str = "Loan Manager API"
    debug: bool = False

    class Config:
        env_file = ".env"


# Instance globale
settings = Settings()
