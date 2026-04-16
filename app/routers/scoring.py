from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies import get_current_user, require_agent_ou_admin
from app.models.user import User
from app.schemas.scoring import ClientScoringInput, ScoringResult, DemandeScoring
from app.services.scoring_service import predire_score

router = APIRouter(prefix="/scoring", tags=["Scoring"])


@router.post("/predire", response_model=ScoringResult)
def predire(
    demande: DemandeScoring,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_agent_ou_admin),
):
    """
    Prédit le score de risque d'un client et calcule la quotité recommandée.
    Accessible aux agents et admins.
    """
    try:
        result = predire_score(demande.client_input)
        result.montant_finançable = round(
            demande.prix_telephone * result.quotite_recommandee, 2
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/predire-rapide", response_model=ScoringResult)
def predire_rapide(
    client: ClientScoringInput, current_user: User = Depends(require_agent_ou_admin)
):
    """
    Prédit uniquement le score sans créer de demande.
    Utile pour tester rapidement un profil client.
    """
    try:
        return predire_score(client)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
