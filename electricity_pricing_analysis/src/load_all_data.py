import pandas as pd

def load_weather_average(file_dict):
    dfs = []
    for city, path in file_dict.items():
        df = pd.read_csv(path, skiprows=2)
        df.columns = ["datetime", city]
        df["datetime"] = pd.to_datetime(df["datetime"])
        df[city] = df[city].astype(float)
        dfs.append(df)
    df_weather = dfs[0]
    for df in dfs[1:]:
        df_weather = df_weather.merge(df, on="datetime")
    df_weather["temperature_avg_c"] = df_weather.drop(columns=["datetime"]).mean(axis=1)
    return df_weather[["datetime", "temperature_avg_c"]]

def load_erzeugung(path):
    df = pd.read_csv(path, sep=";", encoding="utf-8", low_memory=False)
    df = df[[
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

def load_preise(path):
    df = pd.read_csv(path, sep=";", encoding="utf-8", low_memory=False)
    df = df[["Datum von", "Deutschland/Luxemburg [€/MWh] Originalauflösungen"]].copy()
    df.columns = ["datetime", "price_eur_mwh"]
    df["datetime"] = pd.to_datetime(df["datetime"], format="%d.%m.%Y %H:%M")
    df["price_eur_mwh"] = df["price_eur_mwh"].str.replace(",", ".").astype(float)
    return df

def merge_all(weather_dict, erzeugung_path, preis_path):
    weather = load_weather_average(weather_dict)
    erzeugung = load_erzeugung(erzeugung_path)
    preis = load_preise(preis_path)
    return preis.merge(weather, on="datetime").merge(erzeugung, on="datetime")
