from google.cloud import bigquery
import pandas as pd

def fetch_clean_data() -> pd.DataFrame:
    '''
    Fetches cleaned data from BigQuery and feeds it into pandas DataFrames.

    :returns: :object:
        Returns a pandas DataFrame object with rows in the '_clean' views.
    :rtype: pd.DataFrame
    '''

    # Initialize bigquery client and set values for project, dataset and table.
    try:
        bigquery_client = bigquery.Client()
    except Exception as e:
        # Prints potential error message (which will appear in google cloud logging by default).
        print(f'Failed to initialize bigquery client: {e}')
        # Returns string used as indicator for jsonify error message in main.
        return 'not found'
    
    project_id = 'acquired-sound-433108-c6'
    oxygen_dataset = 'oxygen_data'
    weather_dataset = 'weather_data'
    oxygen_view = 'oxygen_clean'
    weather_view = 'weather_clean'

    # Defines query that's going to be used on the bigquery view.
    query = (f'''SELECT
                 w.dt,
                 w.temp,
                 o.oxygen_d1
                 FROM `{project_id}.{oxygen_dataset}.{oxygen_view}` AS o
                 INNER JOIN `{project_id}.{weather_dataset}.{weather_view}` AS w
                 ON ABS(DATE_DIFF(o.datetime_utc, w.datetime_utc, SECOND)) < 300
                 ORDER BY dt DESC''')

    try:
        # Uses query on bigquery "as a whole" (which is why project and dataset is specified above).
        query_job = bigquery_client.query(query)

        # Fetches the resulting data from the query.
        results = query_job.result()

        joined_df = results.to_dataframe()

        return joined_df
    except Exception as e:
        # Prints potential error message (which will appear in google cloud logging by default).
        print(f'fetching bigquery oxygen_clean failed: {e}')
        # Returns string used as indicator for jsonify error message in main.
        return 'not found'