from pydantic import BaseModel, EmailStr
from app.models.user import RoleEnum


class UserCreate(BaseModel):
    nom: str
    email: EmailStr
    mot_de_passe: str
    role: RoleEnum = RoleEnum.agent


class UserLogin(BaseModel):
    email: EmailStr
    mot_de_passe: str


class UserResponse(BaseModel):
    id: int
    nom: str
    email: str
    role: RoleEnum
    est_actif: bool

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
