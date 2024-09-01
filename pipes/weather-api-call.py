import json, requests, io
from google.cloud import bigquery

api_url = 'https://api.openweathermap.org/data/2.5/weather?lat=59.33&lon=18.06&appid=7e1002f883711d56d3add2b3cab45ba5'

bigquery_client = bigquery.Client('acquired-sound-433108-c6') # bigquery project id
dataset = bigquery_client.dataset('weather_raw') # bigquery dataset
table = dataset.table('json_table') # bigquery table

# Fetches data from weather api and transforms it into json (python dict).
response = requests.get(api_url)
weather_data = response.json()

# For some reason the 'weather' value was a dictionary inside a list. Moves it out of the list to create a more "uniform" structure.
weather_data['weather'] = weather_data['weather'][0]

# Turns the json (dict) into a binary data json string, as requires by the bigquery.Client.load_table_from_file() function.
weather_data_binary = io.StringIO(json.dumps(weather_data))

# Gets and changes job_config to allow for automatic table schema determination based on json.
# Technically this is a schema, but since it's automatically determined by incoming data it's practically schemaless.
job_config = bigquery.LoadJobConfig() # Gets job_config.
job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON # Newline_delimited_json changes how json is read.
job_config.schema_update_options = ['ALLOW_FIELD_ADDITION', 'ALLOW_FIELD_RELAXATION'] # Sets job_config to allow creating new fields/columns.
job_config.autodetect = True # Tells job_config to automatically determine schema.

# Loads binary json string as a json file to bigquery table with the changed job_config settings.
job = bigquery_client.load_table_from_file(
    weather_data_binary, 
    table, 
    job_config=job_config
)