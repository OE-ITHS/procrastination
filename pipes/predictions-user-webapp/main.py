from flask import Flask, request, render_template, redirect, url_for, jsonify
from bigquery_predictions import fetch_bq_predictions
from formatter import format_data
import pandas as pd

# Create Flask WSGI application instance.
app = Flask(__name__)

@app.route('/', methods=['GET'])
def web_page():

    # Sets bool for whether data table should be shown in webpage or not. Used for pythonic {% if %} in index.html
    table_bool = False

    if 'show_table' in request.args:
        # Sets bool to true if the GET request includes "show_table".
        table_bool = True

        df = fetch_bq_predictions()

        # Checks if returned df variable is a pandas DataFrame (or the 'not found' string)
        if not isinstance(df, pd.DataFrame):
            # Return descriptive error message
            return jsonify({'error': 'Failed to fetch weather predictions'}), 500

        df = format_data(df)

        # Checks if returned df variable is a pandas DataFrame (or the 'invalid data structure' string)
        if not isinstance(df, pd.DataFrame):
            # Return descriptive error message
            return jsonify({'error': 'Failed to transform weather prediction data'}), 500

        # Changed column names on webpage because bigquery names are short and concise but not as visually appealing.
        column_names = ['predicted_temp', 'data_dt', 'prediction_dt', 'timeframe_start', 'timeframe_end']

        # Calls flask.render_template and references index.html, as well as inputting the dataframe and variables necessary for pythonic if:s.
        return render_template("index.html", column_names=column_names, row_data=list(df.values.tolist()),
                            link_column="df index", zip=zip, table_bool=table_bool)

    # Returns same flask.render_template as above but without the dataframe or dataframe-related variables, since it's not supposed to display the data-table.
    return render_template("index.html", table_bool=table_bool)

@app.route('/clear_table', methods=['GET'])
def clear_table():
    # Redirect to the base URL, which clears the table (since no 'show_table' param will be present)
    # Triggered by second button that appears when the table is displayed.
    return redirect(url_for('web_page'))

if __name__ == '__main__':
    # Run the application on port 8080.
    app.run(host='0.0.0.0', port=8080)