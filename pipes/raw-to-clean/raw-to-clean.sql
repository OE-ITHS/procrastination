CREATE OR REPLACE VIEW `acquired-sound-433108-c6.weather_data.weather_clean` AS

SELECT

  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.coord.lon') AS FLOAT64) AS longitude,
  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.coord.lat') AS FLOAT64) AS latitude,

  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.weather[0].id') AS INT64) AS weather_id,
  JSON_EXTRACT_SCALAR(json_raw, '$.weather[0].main') AS weather_main,
  JSON_EXTRACT_SCALAR(json_raw, '$.weather[0].description') AS weather_description,
  JSON_EXTRACT_SCALAR(json_raw, '$.weather[0].icon') AS weather_icon,

  JSON_EXTRACT_SCALAR(json_raw, '$.base') AS base_station, --internal param

  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.main.temp') AS FLOAT64) AS temperature,
  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.main.feels_like') AS FLOAT64) AS feels_like,
  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.main.temp_min') AS FLOAT64) AS temperature_min,
  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.main.temp_max') AS FLOAT64) AS temperature_max,
  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.main.pressure') AS INT64) AS pressure,
  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.main.humidity') AS INT64) AS humidity,
  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.main.sea_level') AS INT64) AS sea_level_pressure,
  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.main.grnd_level') AS INT64) AS ground_level_pressure,

  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.visibility') AS INT64) AS visibility,

  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.wind.speed') AS FLOAT64) AS wind_speed,
  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.wind.deg') AS INT64) AS wind_direction,
  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.wind.gust') AS FLOAT64) AS wind_gust,

  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.rain.1h') AS FLOAT64) AS precipitaion_1h,
  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.rain.3h') AS FLOAT64) AS precipitaion_3h,

  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.snow.1h') AS FLOAT64) AS snowfall_1h,
  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.snow.3h') AS FLOAT64) AS snowfall_3h,

  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.clouds.all') AS INT64) AS cloudiness_procent,
  
  -- Convert epoch timestamps to UTC
  TIMESTAMP_SECONDS(CAST(JSON_EXTRACT_SCALAR(json_raw, '$.dt') AS INT64)) AS observation_time_utc,
  TIMESTAMP_SECONDS(CAST(JSON_EXTRACT_SCALAR(json_raw, '$.sys.sunrise') AS INT64)) AS sunrise_utc,
  TIMESTAMP_SECONDS(CAST(JSON_EXTRACT_SCALAR(json_raw, '$.sys.sunset') AS INT64)) AS sunset_utc,
  
  JSON_EXTRACT_SCALAR(json_raw, '$.sys.country') AS country,
  JSON_EXTRACT_SCALAR(json_raw, '$.name') AS city_name,
  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.timezone') AS INT64) AS timezone_offset,
  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.id') AS INT64) AS city_id,
  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.cod') AS INT64) AS cod_status
  
FROM `acquired-sound-433108-c6.weather_data.weather_raw`
LIMIT 10; 