from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import traceback
from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse, Token
from app.utils.security import hasher_mot_de_passe, verifier_mot_de_passe
from app.utils.jwt import creer_token
from app.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentification"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    try:
        existant = db.query(User).filter(User.email == user_data.email).first()
        if existant:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cet email est deja utilise",
            )
        nouveau = User(
            nom=user_data.nom,
            email=user_data.email,
            mot_de_passe=hasher_mot_de_passe(user_data.mot_de_passe),
            role=user_data.role,
        )
        db.add(nouveau)
        db.commit()
        db.refresh(nouveau)
        return nouveau
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.email == credentials.email).first()
        if not user or not verifier_mot_de_passe(
            credentials.mot_de_passe, user.mot_de_passe
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ou mot de passe incorrect",
            )
        if not user.est_actif:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Compte desactive"
            )
        token = creer_token({"sub": str(user.id), "role": user.role})
        return {"access_token": token, "token_type": "bearer"}
    except HTTPException:
        raise
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user
