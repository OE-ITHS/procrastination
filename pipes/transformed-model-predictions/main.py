from flask import Flask, jsonify
import pandas as pd
import joblib, xgboost
from bigquery_weather import fetch_bq_data
from transform import transform_data

app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def make_predictions():

    try:
        model = joblib.load('./ml-model/weather_forecasting_model_stockholm_xgb.pkl')
    except Exception as e:
        print(f'Failed to load xgb model: {e}')
        return jsonify({'error': 'Failed to load xgb model'}), 500

    df = fetch_bq_data()

    if df == 'not found':
        # Return descriptive error message
        return jsonify({'error': 'Failed to fetch weather data'}), 500

    if 'temp_lag_3' not in df.columns:
        try:
            df = transform_data(df)
        except Exception as e:
            # Provide descriptive error message
            print(f'Failed to transform data: {e}')
            return jsonify({'error': 'Failed to transform data: Invalid data structure'}), 500

    X = df[['hour', 'month', 'temp','humidity','pressure','temp_lag_1','temp_lag_3']]

    try:
        y_pred = model.predict(X)
    except Exception as e:
        print(f'model.predict failed: {e}')
        return jsonify({'error': 'Failed to predict temperature'}), 500

    current_prediction = y_pred[-1]

    return jsonify({'message': f'Prediction: {current_prediction}'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)