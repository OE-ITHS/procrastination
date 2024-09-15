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
        bigquery.SchemaField(name="temp_pred",     field_type="FLOAT64",   description="Predicted max temperature for following 24 hour period (not counting current hour)."),
        bigquery.SchemaField(name="data_dt",       field_type="TIMESTAMP", description="Datetime of \"base\" data row used for prediction. UTC."                            ),
        bigquery.SchemaField(name="pred_dt",       field_type="TIMESTAMP", description="Datetime prediction was made. UTC."                                                 ),
        bigquery.SchemaField(name="pred_start_dt", field_type="TIMESTAMP", description="Starting datetime of 24 hour period the predicted temperature applies for. UTC."    ),
        bigquery.SchemaField(name="pred_end_dt",   field_type="TIMESTAMP", description="Ending datetime of 24 hour period the predicted temperature applies for. UTC."      )
    ]

    # Creates more descriptive datetime for swedish time relative to UTC.
    sweTZobject = timezone(timedelta(hours=1), name='SWE')

    # Sets the datetime of the used data to a variable for use below.
    data_dt = datetime.fromtimestamp(used_data_datetime)

    # Create pandas dataframe with temp_pred and datetime of prediction.
    df = pd.DataFrame({
        'temp_pred':weather_prediction, 
        'data_dt':data_dt,
        'pred_dt':datetime.today().astimezone(sweTZobject),
        'pred_start_dt':data_dt + timedelta(hours=1),
        'pred_end_dt':data_dt + timedelta(days=1, hours=1)
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