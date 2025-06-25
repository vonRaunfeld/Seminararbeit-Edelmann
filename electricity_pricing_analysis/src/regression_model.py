# src/regression_model.py

import pandas as pd
from sklearn.preprocessing import StandardScaler

def load_and_prepare_data(csv_path="electricity_pricing_analysis/data/merged_dataset.csv"):
    df = pd.read_csv(csv_path, parse_dates=["datetime"])
    
    features = ["temperature_avg_c", "solar_mwh", "wind_onshore_mwh", "wind_offshore_mwh"]
    target = "price_eur_mwh"
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(df[features])
    y = df[target]
    
    X_scaled_df = pd.DataFrame(X_scaled, columns=features)
    return X_scaled_df, y
