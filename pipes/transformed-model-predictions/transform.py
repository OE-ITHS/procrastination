import pandas as pd

def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Temporary function meant for testing transformed-model-predictions without having to wait for weather-transformed-view.sql to be finished and deployed
    '''

    # Generate time-based features
    df['hour'] = pd.to_datetime(df['dt'], unit='s').dt.hour
    df['month'] = pd.to_datetime(df['dt'], unit='s').dt.month
    
    # Generate lag features (e.g., temperature 1 hour ago)
    df['temp_lag_1'] = df['temp'].shift(1)
    df['temp_lag_3'] = df['temp'].shift(3)

    # Feature selection (yes I'm copying from Esoon's github)
    parsed_df = df[['hour', 'month', 'temp', 'humidity', 'pressure', 'temp_lag_1', 'temp_lag_3']]

    parsed_df = parsed_df.dropna()

    # Prints number of pd.DataFrame rows that is used for .predict() to gcp logging to make sure it's only 1 row.
    print(f'Pandas DataFrame has {parsed_df.rows} number of rows after transformation and .dropna().')

    return parsed_df