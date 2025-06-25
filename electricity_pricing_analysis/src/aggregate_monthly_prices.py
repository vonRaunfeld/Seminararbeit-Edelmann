import pandas as pd

def create_monthly_price_average(input_path, output_path):
    """
    Aggregiert stündliche Strompreise zu monatlichen Durchschnittswerten.

    Args:
        input_path (str): Pfad zur CSV mit stündlichem merged_dataset.
        output_path (str): Pfad zur Zieldatei (monatlicher Mittelwert).
    """
    df = pd.read_csv(input_path, parse_dates=["datetime"])
    df['month'] = df['datetime'].dt.to_period('M').dt.to_timestamp()
    
    df_monthly = df.groupby('month')['price_eur_mwh'].mean().reset_index()
    df_monthly.rename(columns={'month': 'date'}, inplace=True)
    
    df_monthly.to_csv(output_path, index=False)
