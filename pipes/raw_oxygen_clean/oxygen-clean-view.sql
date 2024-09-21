CREATE OR REPLACE VIEW `acquired-sound-433108-c6.oxygen_data.oxygen_clean` AS

SELECT

  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.updated') AS INT64) AS dt,
  TIMESTAMP_MILLIS(CAST(JSON_EXTRACT_SCALAR(json_raw, '$.updated') AS INT64)) AS datetime_utc,

  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.position[0].latitude') AS FLOAT64) AS latitude,
  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.position[0].longitude') AS FLOAT64) AS longitude,

  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.value_d1.value') AS FLOAT64) AS oxygen_d1,
  JSON_EXTRACT_SCALAR(json_raw, '$.value_d1.quality') AS quality_d1,

  CAST(JSON_EXTRACT_SCALAR(json_raw, '$.value_d5.value') AS FLOAT64) AS oxygen_d5,
  JSON_EXTRACT_SCALAR(json_raw, '$.value_d5.quality') AS quality_d5

FROM `acquired-sound-433108-c6.oxygen_data.oxygen_raw`