import pandas as pd
import numpy as np
import re
import joblib
import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import classification_report, accuracy_score
from xgboost import XGBClassifier


def nettoyer_valeur_numerique(val):
    if pd.isna(val):
        return np.nan
    val_str = str(val).strip()
    val_str = re.sub(r"[^0-9.\-]", "", val_str)
    try:
        return float(val_str)
    except:
        return np.nan


def charger_et_preparer(chemin="data/train.csv"):
    print("Chargement des données...")
    df = pd.read_csv(chemin, low_memory=False)

    colonnes_inutiles = ["ID", "Customer_ID", "Name", "SSN", "Month", "Type_of_Loan"]
    df = df.drop(columns=[c for c in colonnes_inutiles if c in df.columns])

    colonnes_numeriques = [
        "Age",
        "Annual_Income",
        "Monthly_Inhand_Salary",
        "Num_Bank_Accounts",
        "Num_Credit_Card",
        "Interest_Rate",
        "Num_of_Loan",
        "Delay_from_due_date",
        "Num_of_Delayed_Payment",
        "Changed_Credit_Limit",
        "Num_Credit_Inquiries",
        "Outstanding_Debt",
        "Credit_Utilization_Ratio",
        "Total_EMI_per_month",
        "Amount_invested_monthly",
        "Monthly_Balance",
    ]

    for col in colonnes_numeriques:
        if col in df.columns:
            df[col] = df[col].apply(nettoyer_valeur_numerique)
            df[col] = df[col].fillna(df[col].median())

    colonnes_categorielles = [
        "Occupation",
        "Credit_Mix",
        "Payment_of_Min_Amount",
        "Payment_Behaviour",
    ]

    le = LabelEncoder()
    for col in colonnes_categorielles:
        if col in df.columns:
            df[col] = df[col].fillna("Unknown")
            df[col] = le.fit_transform(df[col].astype(str))

    if "Credit_History_Age" in df.columns:

        def extraire_mois(val):
            if pd.isna(val):
                return 0
            match = re.search(r"(\d+)\s*Years?\s*and\s*(\d+)\s*Months?", str(val))
            if match:
                return int(match.group(1)) * 12 + int(match.group(2))
            match = re.search(r"(\d+)\s*Years?", str(val))
            if match:
                return int(match.group(1)) * 12
            return 0

        df["Credit_History_Age"] = df["Credit_History_Age"].apply(extraire_mois)

    mapping_risque = {"Good": 0, "Standard": 1, "Poor": 2}
    df["Credit_Score"] = df["Credit_Score"].map(mapping_risque)
    df = df.dropna(subset=["Credit_Score"])

    return df


def entrainer_modele(df):
    print("Entraînement du modèle XGBoost...")
    X = df.drop(columns=["Credit_Score"])
    y = df["Credit_Score"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    modele = XGBClassifier(
        n_estimators=200,
        max_depth=6,
        learning_rate=0.1,
        use_label_encoder=False,
        eval_metric="mlogloss",
        random_state=42,
    )

    modele.fit(X_train, y_train)

    y_pred = modele.predict(X_test)
    print("\nRésultats du modèle :")
    print(f"Précision globale : {accuracy_score(y_test, y_pred):.2%}")
    print("\nRapport détaillé :")
    print(
        classification_report(y_test, y_pred, target_names=["Good", "Standard", "Poor"])
    )

    os.makedirs("data/modele", exist_ok=True)
    joblib.dump(modele, "data/modele/xgboost_scoring.pkl")
    joblib.dump(list(X.columns), "data/modele/features.pkl")
    print("\nModèle sauvegardé dans data/modele/")

    return modele, list(X.columns)


def calculer_quotite(score_classe, probabilites):
    prob_poor = probabilites[2]
    if prob_poor < 0.20:
        quotite = round(0.90 - prob_poor, 2)
        categorie = "faible"
    elif prob_poor < 0.40:
        quotite = round(0.70 - prob_poor * 0.5, 2)
        categorie = "moyen"
    elif prob_poor < 0.65:
        quotite = round(0.45 - prob_poor * 0.3, 2)
        categorie = "eleve"
    else:
        quotite = round(max(0.05, 0.20 - prob_poor * 0.1), 2)
        categorie = "critique"
    return max(0.05, min(0.90, quotite)), categorie


if __name__ == "__main__":
    df = charger_et_preparer("data/train.csv")
    print(f"Données prêtes : {df.shape}")
    modele, features = entrainer_modele(df)
    print("\nPipeline ML terminé avec succès !")
