import pandas as pd
import statsmodels.api as sm

def run_monthly_battery_regression(price_path, battery_path):
    """
    Führt eine lineare Regression durch: Monatsmittel Strompreis ~ Batteriekapazität (GWh)
    
    Args:
        price_path (str): Pfad zur CSV mit monatlichem Preis-Durchschnitt
        battery_path (str): Pfad zur CSV mit monatlicher Speicherkapazität
    
    Returns:
        results: Regressionsergebnisse (statsmodels)
    """
    # Lade Daten
    df_price = pd.read_csv(price_path, parse_dates=["date"])
    df_battery = pd.read_csv(battery_path, parse_dates=["date"])

    # Mergen
    df_monthly = pd.merge(df_price, df_battery, on="date", how="inner")

    # Regression
    X = sm.add_constant(df_monthly["battery_capacity_gwh"])
    y = df_monthly["price_eur_mwh"]
    model = sm.OLS(y, X)
    results = model.fit()

    return results
