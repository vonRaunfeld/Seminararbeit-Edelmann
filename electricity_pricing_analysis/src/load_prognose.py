# src/load_prognose.py

import pandas as pd

def load_erzeugung_prognose(csv_path):
    """
    Lädt und verarbeitet die Prognose-Daten von SMARD.de (erneuerbare Einspeisung).
    
    Args:
        csv_path (str): Pfad zur heruntergeladenen CSV-Datei
    
    Returns:
        pd.DataFrame: Zeitreihe mit Spalten: datetime, solar_mwh, wind_onshore_mwh, wind_offshore_mwh
    """
    df_raw = pd.read_csv(csv_path, sep=';', encoding='utf-8', low_memory=False)

    df = df_raw[[
        "Datum von",
        "Photovoltaik [MWh] Berechnete Auflösungen",
        "Wind Onshore [MWh] Berechnete Auflösungen",
        "Wind Offshore [MWh] Berechnete Auflösungen"
    ]].copy()

    df.columns = ["datetime", "solar_mwh", "wind_onshore_mwh", "wind_offshore_mwh"]
    df["datetime"] = pd.to_datetime(df["datetime"], format="%d.%m.%Y %H:%M")

    for col in ["solar_mwh", "wind_onshore_mwh", "wind_offshore_mwh"]:
        df[col] = df[col].str.replace(".", "", regex=False)
        df[col] = df[col].str.replace(",", ".", regex=False).astype(float)

    return df
