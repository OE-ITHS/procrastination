from flask import Flask, jsonify
from api_oxygen import fetch_oxygen_data
from oxygen_bigquery import get_schema, generate_df_and_config, load_to_bigquery

# Create Flask WSGI application instance.
app = Flask(__name__)

@app.route('/oxygen', methods=['GET'])
def api_oxygen_bq(request):
    oxygen_data = fetch_oxygen_data()
    
    # Provide descriptive error messages.
    if oxygen_data is None:
        return jsonify({'error': 'Failed to fetch oxygen data'}), 500
    
    schema = get_schema()

    oxygen_df, job_config = generate_df_and_config(oxygen_data, schema)

    if not load_to_bigquery(oxygen_df, job_config):
        return jsonify({'error': 'Failed to load data to BigQuery'}), 500
    return jsonify({'message': 'Data stored successfully!'})

if __name__ == '__main__':
    # Run the application on port 8080.
    app.run(host='0.0.0.0', port=8080)