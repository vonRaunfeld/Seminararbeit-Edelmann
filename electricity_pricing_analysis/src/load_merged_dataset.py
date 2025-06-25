# src/load_merged_dataset.py

import pandas as pd

def load_merged_dataset(csv_path="electricity_pricing_analysis/data/merged_dataset.csv"):
    """
    Lädt den vollständig vorbereiteten, zusammengeführten Datensatz mit
    Preis, Wetter und prognostizierter EE-Erzeugung.

    Args:
        csv_path (str): Pfad zur gespeicherten CSV-Datei

    Returns:
        pd.DataFrame: DataFrame mit den Spalten:
                      datetime, price_eur_mwh, temperature_avg_c,
                      solar_mwh, wind_onshore_mwh, wind_offshore_mwh
    """
    df = pd.read_csv(csv_path, parse_dates=["datetime"])
    return df
