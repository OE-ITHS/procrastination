from google.cloud import bigquery
import io, json

def load_data_to_bigquery(weather_data: dict) -> bool:
    '''
    Loads data to a bigquery table with an automatically determined schema based on the data.

    :param weather_data: 
        weather_data is expected to be dictonary generated from response.json() in the api_weather.fetch_current_data() function.
        Directly feed the returned dict object from api_weather.fetch_current_data() into this function.
    :returns: :object:
        Returns True if data successfully loaded to BigQuery or False if data failed to load to BigQuery. See error message.
    :rtype: bool
    '''

    # Initialize BigQuery client.
    bigquery_client = bigquery.Client()
    table_id = 'acquired-sound-433108-c6.weather_raw.json_table'

    # Normalize the 'weather' field.
    if 'weather' in weather_data and isinstance(weather_data['weather'], list):
        weather_data['weather'] = weather_data['weather'][0]

    # Prepare data for BigQuery.
    weather_data_binary = io.StringIO(json.dumps(weather_data))

    # BigQuery job configuration.
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.NEWLINE_DELIMITED_JSON,
        schema_update_options=['ALLOW_FIELD_ADDITION', 'ALLOW_FIELD_RELAXATION'],
        autodetect=True
    )

    try:
        # Load binary data into BigQuery.
        job = bigquery_client.load_table_from_file(
            weather_data_binary,
            table_id,
            job_config=job_config
        )
        # Check if load_table_from_file succeeded or failed. If failed, also provides error message.
        job.result()
        return True
    except Exception as e:
        print(f'Failed to load data to BigQuery: {e}')
        return False