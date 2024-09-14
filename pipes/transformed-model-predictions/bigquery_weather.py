from google.cloud import bigquery
import pandas as pd
import xgboost as xgb

def fetch_bq_data() -> pd.DataFrame:
    '''
    Fetches ingestion-ready data from BigQuery and feeds it into a pandas DataFrame.

    :returns: :object:
        Returns a pandas DataFrame object with all rows in the 'weather_transformed' view.
    :rtype: pd.DataFrame
    '''

    # Initialize bigquery client and set values for project, dataset and table.
    bigquery_client = bigquery.Client()
    project_id = 'acquired-sound-433108-c6'
    dataset_id = 'weather_data'
    table_id = 'weather_transformed'

    try:
        # Creates a pointer (ish) object to the dataset using the project- and dataset id
        dataset_ref = bigquery.DatasetReference(project_id, dataset_id)
        # Creates a pointer (ish) object to the table (on this case a view) using the previous dataset_ref
        table_ref = dataset_ref.table(table_id)
        # Creates a table object with the same data as the actual table on bigquery using the previous table_ref
        table = bigquery_client.get_table(table_ref)

        # Uses the previously initalized bigquery client to list all the rows of the table object and puts them in a (pandas) dataframe.
        df = bigquery_client.list_rows(table).to_dataframe()

        return df
    except Exception as e:
        print(f'fetching bigquery data failed: {e}')
        return 'not found'