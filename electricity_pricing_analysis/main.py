from src.load_prognose import load_erzeugung_prognose
from src.load_multi_city_weather import load_all_cities
from src.load_all_data import merge_all
from src.load_merged_dataset import load_merged_dataset
from src.regression_diagnostics import plot_residuals
from src.monthly_battery_regression import run_monthly_battery_regression
from src.aggregate_monthly_prices import create_monthly_price_average
from src.import_export_regression import run_hourly_import_export_regression

df_erzeugung = load_erzeugung_prognose("electricity_pricing_analysis/data/Prognostizierte_Erzeugung_Day-Ahead_202301010000_202501010000_Stunde.csv")

weather_files = {
    "Hamburg": "electricity_pricing_analysis/data/open-meteo-53.53N9.98E11m-2.csv",
    "Leipzig": "electricity_pricing_analysis/data/open-meteo-51.35N12.35E109m.csv",
    "Köln": "electricity_pricing_analysis/data/open-meteo-50.93N6.91E60m.csv",
    "München": "electricity_pricing_analysis/data/open-meteo-48.12N11.55E524m.csv",
    "Frankfurt": "electricity_pricing_analysis/data/open-meteo-50.09N8.65E117m.csv"
}

df_temp = load_all_cities(weather_files)
print(df_temp.head())

df_all = merge_all(weather_files,
                   "electricity_pricing_analysis/data/Prognostizierte_Erzeugung_Day-Ahead_202301010000_202501010000_Stunde.csv",
                   "electricity_pricing_analysis/data/Gro_handelspreise_202301010000_202501010000_Stunde.csv")

print(df_all.head())

# Speichern des vollständigen Datensatzes als CSV
df_all.to_csv("electricity_pricing_analysis/data/merged_dataset.csv", index=False)
print("Datensatz wurde gespeichert als: data/merged_dataset.csv")

df = load_merged_dataset()
print(df.head())

from src.regression_model import load_and_prepare_data

X, y = load_and_prepare_data()
print(X.head())

from src.run_regression import load_data_for_regression, run_ols_regression

X, y = load_data_for_regression()
results = run_ols_regression(X, y)
print(results.summary())


residuals = results.resid
plot_residuals(residuals)

print("_______________________")
print("Ergebnisse monatliche regression")
print("_______________________")
create_monthly_price_average(
    "electricity_pricing_analysis/data/merged_dataset.csv",
    "electricity_pricing_analysis/data/monthly_price_average.csv"
)



results = run_monthly_battery_regression(
    "electricity_pricing_analysis/data/monthly_price_average.csv",
    "electricity_pricing_analysis/data/Monatliche_Batteriespeicherkapazitaet_GWh.csv"
)

print(results.summary())

print("_______________________")
print("Ergebnisse Regression Import/Export")
print("_______________________")

results = run_hourly_import_export_regression()

