"""
data_loader.py
Chargement et nettoyage des fichiers CSV climatiques telecharges depuis
climat.meteo.gc.ca (donnees journalieres).
Convention de nommage: data/<Ville>_<Annee>.csv
Exemple : data/Ottawa_2026.csv
"""

import os
import pandas as pd

DOSSIER_DONNEES = "data"

# Deux en-tetes possibles selon la langue 
COLONNES_UTILES_FR = {
    "Date/Heure": "date",
    "Temp max.(°C)": "temp_max",
    "Temp min.(°C)": "temp_min",
    "Temp moy.(°C)": "temp_moy",
    "Précip. tot. (mm)": "precip_mm",
}

COLONNES_UTILES_EN = {
    "Date/Time": "date",
    "Max Temp (°C)": "temp_max",
    "Min Temp (°C)": "temp_min",
    "Mean Temp (°C)": "temp_moy",
    "Total Precip (mm)": "precip_mm",
}


class FichierDonneesIntrouvable(Exception):
    """Levee quand le fichier CSV attendu n'existe pas sur le disque."""
    pass


def chemin_fichier(ville: str, annee: str) -> str:
    return os.path.join(DOSSIER_DONNEES, f"{ville}_{annee}.csv")


def charger_donnees(ville: str, annee: str) -> pd.DataFrame:
    """
    Charge et nettoie les donnees climatiques d'une ville pour une annee.

    Retourne un DataFrame avec les colonnes :
    date, mois, temp_max, temp_min, temp_moy, precip_mm
    """
    chemin = chemin_fichier(ville, annee)
    if not os.path.exists(chemin):
        raise FichierDonneesIntrouvable(
            f"Fichier introuvable : {chemin}\n\n"
            f"Telecharge le CSV pour {ville} ({annee}) depuis "
            f"climat.meteo.gc.ca et place-le dans le dossier "
            f"'{DOSSIER_DONNEES}/' sous ce nom exact."
        )

    # encoding="utf-8-sig" gere le caractere invisible (BOM) 
    brut = pd.read_csv(chemin, encoding="utf-8-sig")

    # Determiner si le fichier est en fr ou eng
    if any(c in brut.columns for c in COLONNES_UTILES_FR):
        mapping = COLONNES_UTILES_FR
    else:
        mapping = COLONNES_UTILES_EN

    colonnes_presentes = [c for c in mapping if c in brut.columns]
    manquantes = set(mapping) - set(colonnes_presentes)
    if manquantes:
        print(f"[Avertissement] Colonnes manquantes dans {chemin} : {manquantes}")

    if not colonnes_presentes:
        raise ValueError(
            f"Aucune colonne reconnue dans {chemin}. "
            f"Verifie qu'il s'agit bien d'un export 'journalier' d'ECCC."
        )

    df = brut[colonnes_presentes].rename(columns=mapping)

    if "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df = df.dropna(subset=["date"])
        df["mois"] = df["date"].dt.month
    else:
        df["mois"] = pd.NA

    #  On remplace la virgule par un point avant de convertir en nombre 
    for col in ["temp_max", "temp_min", "temp_moy", "precip_mm"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.replace(",", ".", regex=False)
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def statistiques_mensuelles(df: pd.DataFrame) -> pd.DataFrame:
    """Moyennes de temperature et cumul de precipitations par mois (1 a 12)."""
    agg = {}
    if "temp_max" in df.columns:
        agg["temp_max"] = ("temp_max", "mean")
    if "temp_min" in df.columns:
        agg["temp_min"] = ("temp_min", "mean")
    if "precip_mm" in df.columns:
        agg["precip_mm"] = ("precip_mm", "sum")

    return df.groupby("mois").agg(**agg).reindex(range(1, 13))


def pourcentage_jours_gel(df: pd.DataFrame) -> float:
    """Pourcentage de jours ou la temperature minimale est sous 0 degre C."""
    if "temp_min" not in df.columns:
        return 0.0
    valides = df["temp_min"].dropna()
    if valides.empty:
        return 0.0
    return float((valides < 0).mean() * 100)