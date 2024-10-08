from flask import Flask, jsonify
import pandas as pd
import joblib
from bigquery_weather import fetch_bq_data
from transform import transform_data
from predictions_bigquery import load_prediction_to_bigquery

app = Flask(__name__)

@app.route('/predict', methods=['GET'])
def make_predictions(request):

    try:
        # Load xgboost model from .pkl file generated by Esoon's .ipynb file.
        model = joblib.load('./ml-model/weather_forecasting_model_stockholm_xgb.pkl')
    except Exception as e:
        # Print error message (which automatically gets picked up by google cloud logging).
        print(f'Failed to load xgb model: {e}')
        # Return error message to http request.
        return jsonify({'error': 'Failed to load xgb model'}), 500

    # Fetches cleaned/transformed weather data from bigquery view to use for prediction.
    df = fetch_bq_data()

    # Checks if returned df variable is a pandas DataFrame (of the 'not found' string)
    if not isinstance(df, pd.DataFrame):
        # Return descriptive error message
        return jsonify({'error': 'Failed to fetch weather data'}), 500

    # Checks if query result returned enough rows to perform predictions (4)
    if df.shape[0] < 4:
        # Return descriptive error message
        return jsonify({'error': f'Query returned {df.shape[0]} rows; 4 needed'})

    # Additional data transformation before model predictions.
    try:
        df = transform_data(df)
    except Exception as e:
        # Provide descriptive error message
        print(f'Failed to transform data: {e}')
        return jsonify({'error': 'Failed to transform data: Invalid data structure'}), 500

    # Sets weather data parameters to be used for .predict().
    X = df[['hour', 'month', 'temp','humidity','pressure','temp_lag_1','temp_lag_3']]

    try:
        # Predicts tomorrows max temperature with the single transformed data row fetches from BigQuery.
        y_pred = model.predict(X)
    except Exception as e:
        print(f'model.predict() failed: {e}')
        return jsonify({'error': 'Failed to predict temperature'}), 500

    # Checks if data was successfully loaded to bigquery table and sends corresponding response message.
    if not load_prediction_to_bigquery(y_pred, df['dt'].iloc[0]):
        return jsonify({'error': 'Failed to load prediction to BigQuery'}), 500
    return jsonify({'message': 'Prediction generated and stored successfully!'})

if __name__ == '__main__':
    # Run the application on port 8080.
    app.run(host='0.0.0.0', port=8080)