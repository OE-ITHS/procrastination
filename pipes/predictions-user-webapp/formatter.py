import pandas as pd

def format_data(df: pd.DataFrame) -> pd.DataFrame:
    '''
    Formats data in DataFrame for display on webapp. Returns DataFrame after formatting.
    '''
    try:
        # Creates number-to-string formatting functions for use in pandas.Series.apply() method.
        def apply_format(number):
            return "{:.2f} \N{DEGREE SIGN}C".format(float(number))
        
        # Uses previously defined method to change all temperatured from floats into strings with only 2 digits shown. Looks nicer on webpage.
        df['temp_pred'] = df['temp_pred'].apply(apply_format)

        # For all 4 columns with identically formatted datetime variables, converts to local time (Europe/Stockholm), 
        #                 makes the datetime variable timezone-naive (removes the +0X:00 at the end of the datetime),
        #                 and then changes the format of the datetime to not include seconds, since exact seconds seemed unecessary for display purposes.
        for column_name in ['data_dt', 'pred_dt', 'pred_start_dt', 'pred_end_dt']:
            df[column_name] = pd.to_datetime(df[column_name]).dt.tz_convert('Europe/Stockholm').dt.tz_localize(None).dt.strftime('%b %d %H:%M')

        df['timeframe'] = (pd.to_datetime(df['pred_start_dt']).dt.tz_convert('Europe/Stockholm').dt.tz_localize(None).dt.strftime('%b %d')
                            + '-'
                            + pd.to_datetime(df['pred_end_dt']).dt.tz_convert('Europe/Stockholm').dt.tz_localize(None).dt.strftime('%d, %H:%M'))
        
        df = df.drop(columns=['pred_start_dt', 'pred_end_dt'])

        return df
    except Exception as e:
        # Prints potential error message (which will appear in google cloud logging by default).
        print(f'Transforming weather prediction data failed; invalid data structure: {e}')
        # Returns string used as indicator for jsonify error message in main.
        return 'invalid data structure'