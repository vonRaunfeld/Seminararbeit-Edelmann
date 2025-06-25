# src/load_multi_city_weather.py

import pandas as pd

def load_city_weather(filepath: str, city_name: str) -> pd.DataFrame:
    """
    Lädt und bereinigt eine Open-Meteo CSV-Datei für eine einzelne Stadt.
    Annahme: Temperatur beginnt ab Zeile 3 (skiprows=2).
    """
    df = pd.read_csv(filepath, skiprows=2)
    df.columns = ["datetime", city_name]
    df["datetime"] = pd.to_datetime(df["datetime"])
    df[city_name] = df[city_name].astype(float)
    return df

def load_all_cities(weather_files: dict) -> pd.DataFrame:
    """
    Führt mehrere Städte zusammen und berechnet den stündlichen Durchschnitt.
    
    Args:
        weather_files (dict): Schlüssel = Stadtname, Wert = Dateipfad
    
    Returns:
        pd.DataFrame: datetime + Temperatur pro Stadt + temperature_avg_c
    """
    dfs = [load_city_weather(path, city) for city, path in weather_files.items()]
    merged = dfs[0]
    for df in dfs[1:]:
        merged = merged.merge(df, on="datetime")
    merged["temperature_avg_c"] = merged.drop(columns=["datetime"]).mean(axis=1)
    return merged
