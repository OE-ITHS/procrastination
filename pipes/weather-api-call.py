import json, requests, io
from google.cloud import bigquery

api_url = 'https://api.openweathermap.org/data/2.5/weather?lat=59.33&lon=18.06&appid=7e1002f883711d56d3add2b3cab45ba5'

bigquery_client = bigquery.Client('acquired-sound-433108-c6')
dataset = bigquery_client.dataset('weather_raw')
table = dataset.table('json_table')

response = requests.get(api_url)
weather_data = response.json()

weather_data['weather'] = weather_data['weather'][0]

weather_data_binary = io.StringIO(json.dumps(weather_data))

job_config = bigquery.LoadJobConfig()
job_config.source_format = bigquery.SourceFormat.NEWLINE_DELIMITED_JSON
job_config.schema_update_options = ['ALLOW_FIELD_ADDITION', 'ALLOW_FIELD_RELAXATION']
job_config.autodetect = True

job = bigquery_client.load_table_from_file(
    weather_data_binary, 
    table, 
    job_config=job_config
)