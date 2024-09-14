from google.cloud import bigquery
from datetime import datetime, timezone, timedelta
import pandas as pd

def load_prediction_to_bigquery(weather_prediction: float, used_data_datetime: int) -> bool:
    '''
    Loads predictions to a bigquery table.

    :param weather_prediction: 
        weather_prediction is expected to be a float generated from model.predict().
    :param used_data_datetime:
        used_data_datetime is expected to be the unix time dt of the data used for the .predict(X) function.
    :returns: :object:
        Returns True if data successfully loaded to BigQuery or False if data failed to load to BigQuery. See error message.
    :rtype: bool
    '''

    # Initialize BigQuery client.
    bigquery_client = bigquery.Client()
    table_id = 'acquired-sound-433108-c6.weather_data.weather_prediction'

    # Define schema layout of BigQuery table.
    schema = [
        bigquery.SchemaField("temp_pred", "NUMERIC"),
        bigquery.SchemaField("prediction_datetime", "TIMESTAMP")
    ]

    # Create pandas dataframe with temp_pred and datetime of prediction.
    df = pd.DataFrame({
        'temp_pred':weather_prediction, 
        'prediction_datetime':datetime.fromtimestamp(used_data_datetime)
    })

    # BigQuery job configuration.
    job_config = bigquery.LoadJobConfig(
        schema=schema,
        write_disposition="WRITE_APPEND"
    )

    try:
        # Load data into BigQuery table.
        job = bigquery_client.load_table_from_dataframe(
            df,
            table_id,
            job_config=job_config
        )
        # Check if job succeeded or failed. If failed, also provides error message.
        job.result()
        return True
    except Exception as e:
        print(f'Failed to load data to BigQuery: {e}')
        return False