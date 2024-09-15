import pandas as pd

def format_data(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Formats data in DataFrame for display on webapp. Returns DataFrame after formatting.
    '''
    def apply_format(number):
        return "{:.1}".format(float(number))
    
    df['temp_pred'] = df['temp_pred'].apply(apply_format)

    for column_name in ['data_dt', 'pred_dt', 'pred_start_dt', 'pred_end_dt']:
        df[column_name] = pd.to_datetime(df[column_name]).dt.floor('M')

    return df