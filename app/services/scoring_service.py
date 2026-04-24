import joblib
import numpy as np
import pandas as pd
from app.schemas.scoring import ClientScoringInput, ScoringResult

MODELE_PATH = "data/modele/xgboost_scoring.pkl"
FEATURES_PATH = "data/modele/features.pkl"

_modele = None
_features = None


def charger_modele():
    global _modele, _features
    if _modele is None:
        _modele = joblib.load(MODELE_PATH)
        _features = joblib.load(FEATURES_PATH)
    return _modele, _features


def encoder_categoriel(valeur: str, mapping: dict, defaut: int = 0) -> int:
    return mapping.get(valeur, defaut)


def preparer_features(client: ClientScoringInput) -> pd.DataFrame:
    occupation_mapping = {
        "Scientist": 8,
        "Teacher": 9,
        "Engineer": 3,
        "Entrepreneur": 4,
        "Developer": 2,
        "Lawyer": 6,
        "Media_Manager": 7,
        "Doctor": 1,
        "Journalist": 5,
        "Manager": 0,
        "Musician": 10,
        "Mechanic": 11,
        "Writer": 12,
        "Unknown": 13,
        "Accountant": 14,
    }
    mix_mapping = {"Bad": 0, "Good": 1, "Standard": 2, "Unknown": 3}
    paiement_min_mapping = {"No": 0, "Yes": 1, "NM": 2}
    comportement_mapping = {
        "Low_spent_Small_value_payments": 0,
        "Low_spent_Medium_value_payments": 1,
        "Low_spent_Large_value_payments": 2,
        "High_spent_Small_value_payments": 3,
        "High_spent_Medium_value_payments": 4,
        "High_spent_Large_value_payments": 5,
    }

    data = {
        "Age": client.age,
        "Annual_Income": client.revenu_annuel,
        "Monthly_Inhand_Salary": client.salaire_mensuel,
        "Num_Bank_Accounts": client.nb_comptes_bancaires,
        "Num_Credit_Card": client.nb_cartes_credit,
        "Interest_Rate": client.taux_interet,
        "Num_of_Loan": client.nb_prets,
        "Delay_from_due_date": client.jours_retard,
        "Num_of_Delayed_Payment": client.nb_paiements_retard,
        "Changed_Credit_Limit": client.limite_credit_changee,
        "Num_Credit_Inquiries": client.nb_demandes_credit,
        "Outstanding_Debt": client.dette_en_cours,
        "Credit_Utilization_Ratio": client.taux_utilisation_credit,
        "Credit_History_Age": client.anciennete_credit_mois,
        "Total_EMI_per_month": client.total_emi_mensuel,
        "Amount_invested_monthly": client.montant_investi_mensuel,
        "Monthly_Balance": client.solde_mensuel,
        "Occupation": encoder_categoriel(client.occupation, occupation_mapping),
        "Credit_Mix": encoder_categoriel(client.mix_credit, mix_mapping),
        "Payment_of_Min_Amount": encoder_categoriel(
            client.paiement_minimum, paiement_min_mapping
        ),
        "Payment_Behaviour": encoder_categoriel(
            client.comportement_paiement, comportement_mapping
        ),
    }
    return pd.DataFrame([data])


def calculer_quotite(prob_poor: float) -> tuple[float, str]:
    if prob_poor < 0.20:
        return round(0.90 - prob_poor, 2), "faible"
    elif prob_poor < 0.40:
        return round(0.70 - prob_poor * 0.5, 2), "moyen"
    elif prob_poor < 0.65:
        return round(0.45 - prob_poor * 0.3, 2), "eleve"
    else:
        return round(max(0.05, 0.20 - prob_poor * 0.1), 2), "critique"


def generer_explication(categorie: str, prob_poor: float) -> str:
    explications = {
        "faible": f"Client fiable avec {prob_poor:.0%} de risque de defaut. Financement recommande.",
        "moyen": f"Client avec risque modere ({prob_poor:.0%}). Financement partiel conseille.",
        "eleve": f"Client a risque eleve ({prob_poor:.0%}). Financement limite recommande.",
        "critique": f"Client tres risque ({prob_poor:.0%}). Financement deconseille.",
    }
    return explications.get(categorie, "Analyse non disponible.")


def predire_score(client: ClientScoringInput) -> ScoringResult:
    modele, features = charger_modele()
    df = preparer_features(client)

    for col in features:
        if col not in df.columns:
            df[col] = 0
    df = df[features]

    probabilites = modele.predict_proba(df)[0]
    prob_poor = float(probabilites[2])
    score_normalise = round(float(prob_poor), 4)

    quotite, categorie = calculer_quotite(prob_poor)
    explication = generer_explication(categorie, prob_poor)

    return ScoringResult(
        score_risque=score_normalise,
        probabilite_defaut=prob_poor,
        categorie_risque=categorie,
        quotite_recommandee=quotite,
        explication=explication,
    )
