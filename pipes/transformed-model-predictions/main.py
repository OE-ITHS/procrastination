from flask import Flask, jsonify
import pandas as pd
import joblib
from bigquery_weather import fetch_bq_data

app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def make_predictions():

    model = joblib.load('./ml-model/weather_forecasting_model_stockholm_xgb.pkl')

    df = fetch_bq_data()

    X = df[['hour', 'month', 'temp','humidity','pressure','temp_lag_1','temp_lag_3']]
    # y = df['temp_target']

    y_pred = model.predict(X)

    # Provide descriptive error messages.
    if weather_data is None:
        return jsonify({'error': 'Failed to fetch weather data'}), 500
    if not load_data_to_bigquery(weather_data):
        return jsonify({'error': 'Failed to load data to BigQuery'}), 500
    return jsonify({'message': 'Data stored successfully!'})

    return 'Oh uuuh I dunno'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)