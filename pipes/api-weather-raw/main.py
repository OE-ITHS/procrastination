from flask import Flask, jsonify
from api_weather import fetch_weather_data
from weather_bigquery import load_data_to_bigquery

# Create Flask WSGI application instance.
app = Flask(__name__)

@app.route('/weather', methods=['GET'])
def api_weather_bq():
    weather_data = fetch_weather_data()
    
    # Provide descriptive error messages.
    if weather_data is None:
        return           jsonify({'error': 'Failed to fetch weather data'}), 500
    if not load_data_to_bigquery(weather_data):
        return jsonify({'error': 'Failed to load data to BigQuery'}), 500
    return jsonify({'message': 'Data stored successfully!'})

if __name__ == '__main__':
    # Run the application on port 8080.
    app.run(host='0.0.0.0', port=8080)