# src/load_weather.py

import pandas as pd

def load_temperature_csv(csv_path):
    """
    Lädt stündliche Temperaturdaten von Open-Meteo im CSV-Format.
    
    Args:
        csv_path (str): Pfad zur CSV-Datei
    
    Returns:
        pd.DataFrame: DataFrame mit Spalten 'datetime', 'temperature_c'
    """
    df = pd.read_csv(csv_path)
    
    # Umbenennen der Spalten, falls nötig
    df.columns = [col.lower() for col in df.columns]
    
    if 'time' in df.columns:
        df.rename(columns={'time': 'datetime'}, inplace=True)
    if 'temperature_2m' in df.columns:
        df.rename(columns={'temperature_2m': 'temperature_c'}, inplace=True)
    
    df['datetime'] = pd.to_datetime(df['datetime'])
    
    return df
