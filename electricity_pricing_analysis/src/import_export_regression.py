import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler
from src.regression_diagnostics import plot_residuals
import matplotlib.pyplot as plt
import seaborn as sns

def run_hourly_import_export_regression():
    # Stromverbrauch + Nettoexport einlesen
    df = pd.read_csv("electricity_pricing_analysis/data/last_und_nettoexport_2023_2024.csv", parse_dates=["Zeit"])

    # Großhandelspreise einlesen
    preise = pd.read_csv("electricity_pricing_analysis/data/Gro_handelspreise_202301010000_202501010000_Stunde.csv", sep=";", encoding="utf-8")

    # Zeit verarbeiten und Preisspalte formatieren
    preise["Zeit"] = pd.to_datetime(preise["Datum von"], format="%d.%m.%Y %H:%M")
    preise["Preis (EUR/MWh)"] = (
        preise["Deutschland/Luxemburg [€/MWh] Originalauflösungen"]
        .replace("-", pd.NA)
        .str.replace(",", ".")
        .astype(float)
    )
    preise = preise[["Zeit", "Preis (EUR/MWh)"]]

    # Merge der Daten
    df_merged = pd.merge(df, preise, on="Zeit", how="inner").dropna()

    # Regressionsdaten definieren
    X = df_merged[["Netzlast (MWh)", "Nettoexport (MW)"]]
    y = df_merged["Preis (EUR/MWh)"]

    # Standardisierung
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Konstante für Regressionsmodell hinzufügen
    X_scaled = sm.add_constant(X_scaled)

    # Regression mit statsmodels
    model = sm.OLS(y, X_scaled).fit()

    # Ergebnisse anzeigen
    print(model.summary())

    # Standardisierung der Regressoren (wie im Modell)
    X = df_merged[["Netzlast (MWh)", "Nettoexport (MW)"]]
    y = df_merged["Preis (EUR/MWh)"]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # In DataFrame umwandeln für Plot
    df_plot = pd.DataFrame(X_scaled, columns=["Netzlast_std", "Nettoexport_std"])
    df_plot["Preis"] = y.values

    # Scatterplot mit Regressionslinie für Netzlast
    plt.figure(figsize=(8,5))
    sns.regplot(x="Netzlast_std", y="Preis", data=df_plot, line_kws={"color": "red"})
    plt.title("Zusammenhang zwischen standardisierter Netzlast und Strompreis")
    plt.xlabel("Netzlast (standardisiert)")
    plt.ylabel("Preis (EUR/MWh)")
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8,5))
    sns.regplot(x="Nettoexport_std", y="Preis", data=df_plot, line_kws={"color": "red"})
    plt.title("Zusammenhang zwischen standardisiertem Nettoexport und Strompreis")
    plt.xlabel("Nettoexport (standardisiert)")
    plt.ylabel("Preis (EUR/MWh)")
    plt.tight_layout()
    plt.show()

    # Residuen berechnen (falls noch nicht vorhanden)
    #residuals = model.resid
    #plot_residuals(residuals)




