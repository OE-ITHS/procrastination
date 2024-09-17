from google.cloud import bigquery
import pandas as pd

def fetch_bq_data() -> pd.DataFrame:
    '''
    Fetches ingestion-ready data from BigQuery and feeds it into a pandas DataFrame.

    :returns: :object:
        Returns a pandas DataFrame object with all rows in the 'weather_clean' view.
    :rtype: pd.DataFrame
    '''

    # Initialize bigquery client and set values for project, dataset and table.
    bigquery_client = bigquery.Client()
    project_id = 'acquired-sound-433108-c6'
    dataset_id = 'weather_data'
    view_id = 'weather_clean'

    # Defines query that's going to be used on the bigquery view.
    query = f'SELECT * FROM `{project_id}.{dataset_id}.{view_id}` ORDER BY dt DESC LIMIT 4'

    try:
        # Uses query on bigquery "as a while" (which is why project and dataset is specified above).
        query_job = bigquery_client.query(query)

        # Fetches the resulting data from the query.
        results = query_job.result()

        df = results.to_dataframe()

        return df
    except Exception as e:
        # Prints potential error message (which will appear in google cloud logging by default).
        print(f'fetching bigquery data failed: {e}')
        # Returns string used as indicator for jsonify error message in main.
        return 'not found'