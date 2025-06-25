# src/run_regression.py

import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler

def load_data_for_regression(csv_path="electricity_pricing_analysis/data/merged_dataset.csv"):
    df = pd.read_csv(csv_path, parse_dates=["datetime"])
    
    X_cols = ["temperature_avg_c", "solar_mwh", "wind_onshore_mwh", "wind_offshore_mwh"]
    y_col = "price_eur_mwh"
    
    # Standardisieren
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[X_cols])
    X_scaled_df = pd.DataFrame(X_scaled, columns=X_cols)
    
    return X_scaled_df, df[y_col]

def run_ols_regression(X, y):
    X = sm.add_constant(X)  # fügt Intercept (β₀) hinzu
    model = sm.OLS(y, X)
    results = model.fit()
    return results
