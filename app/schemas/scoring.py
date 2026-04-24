from pydantic import BaseModel
from typing import Optional


class ClientScoringInput(BaseModel):
    age: float
    revenu_annuel: float
    salaire_mensuel: float
    nb_comptes_bancaires: float
    nb_cartes_credit: float
    taux_interet: float
    nb_prets: float
    jours_retard: float
    nb_paiements_retard: float
    limite_credit_changee: float
    nb_demandes_credit: float
    dette_en_cours: float
    taux_utilisation_credit: float
    anciennete_credit_mois: float
    total_emi_mensuel: float
    montant_investi_mensuel: float
    solde_mensuel: float
    occupation: Optional[str] = "Unknown"
    mix_credit: Optional[str] = "Standard"
    paiement_minimum: Optional[str] = "No"
    comportement_paiement: Optional[str] = "Low_spent_Small_value_payments"


class ScoringResult(BaseModel):
    score_risque: float
    probabilite_defaut: float
    categorie_risque: str
    quotite_recommandee: float
    montant_financable: Optional[float] = None
    explication: str


class DemandeScoring(BaseModel):
    client_input: ClientScoringInput
    prix_telephone: float
    modele_telephone: str
