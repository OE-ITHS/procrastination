from ..pipes.api_weather_raw.api_weather import fetch_weather_data
from ..pipes.api_weather_raw.weather_bigquery import get_schema, generate_df_and_config
from pandas import DataFrame
from google.cloud.bigquery import SchemaField, LoadJobConfig

weather_data = fetch_weather_data()

### api_weather

def test_fetch_weather_data():
    assert isinstance(weather_data, dict) or weather_data is None

### weather_bigquery

def test_get_schema():
    return_object = get_schema()
    assert len(return_object) == 2
    assert all(isinstance(ro, SchemaField) for ro in return_object)

def test_generate_df_and_config():
    df, conf = generate_df_and_config(weather_data, get_schema())
    assert isinstance(df, DataFrame)
    assert set(df.columns) == set(['json_raw', 'ingestion_date_UTC'])
    assert isinstance(conf, LoadJobConfig)
    assert conf.write_disposition == 'WRITE_APPEND'

# Can't really test load_to_bigquery() since every time I run the function it would actually load the data row to bigquery.