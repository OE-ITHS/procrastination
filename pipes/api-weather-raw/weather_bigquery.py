from google.cloud import bigquery
import json
from datetime import datetime, timezone, timedelta
import pandas as pd

def load_data_to_bigquery(weather_data: dict) -> bool:
    '''
    Loads data to a bigquery table with a "schemaless" table, e.i. stored as one value.

    :param weather_data: 
        weather_data is expected to be dictonary generated from response.json() in the api_weather.fetch_current_data() function.
        Directly feed the returned dict object from api_weather.fetch_current_data() into this function.
    :returns: :object:
        Returns True if data successfully loaded to BigQuery or False if data failed to load to BigQuery. See error message.
    :rtype: bool
    '''

    # Initialize BigQuery client.
    bigquery_client = bigquery.Client()
    table_id = 'acquired-sound-433108-c6.weather_data.weather_raw'

    # Transforms weather_data from json to json string for "schemaless" storage.
    # (Entire json stored as one single column and row value)
    weather_data_string = json.dumps(weather_data)

    # Define schema layout of BigQuery table.
    schema = [
        bigquery.SchemaField(name="json_raw",           field_type="STRING",    description="JSON received from API request in string format."),
        bigquery.SchemaField(name="ingestion_date_UTC", field_type="TIMESTAMP", description="Datetime that request was made to API. UTC.")
    ]

    # Creates more descriptive datetime for UTC+1.
    sweTZobject = timezone(timedelta(hours=1), name='SWE')

    # Create pandas dataframe with json_data and datetime of ingestion.
    df = pd.DataFrame({
        'json_raw':[weather_data_string], 
        'ingestion_date_UTC':datetime.today().astimezone(sweTZobject)
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