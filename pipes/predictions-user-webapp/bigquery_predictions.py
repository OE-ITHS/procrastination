from google.cloud import bigquery
import pandas as pd

def fetch_bq_predictions() -> pd.DataFrame:
    '''
    Fetches already-made predictions from BigQuery and feeds it into a pandas DataFrame.

    :returns: :object:
        Returns a pandas DataFrame object with all rows in the 'weather_predictions' view.
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
    dataset_id = 'weather_data'
    view_id = 'weather_prediction'

    # Defines query that's going to be used on the bigquery view.
    query = f'SELECT * FROM `{project_id}.{dataset_id}.{view_id}` ORDER BY pred_dt DESC LIMIT 12'

    try:
        # Uses query on bigquery "as a whole" (which is why project and dataset is specified above).
        query_job = bigquery_client.query(query)

        # Fetches the resulting data from the query.
        results = query_job.result()

        df = results.to_dataframe()

        return df
    except Exception as e:
        # Prints potential error message (which will appear in google cloud logging by default).
        print(f'fetching bigquery predictions failed: {e}')
        # Returns string used as indicator for jsonify error message in main.
        return 'not found'