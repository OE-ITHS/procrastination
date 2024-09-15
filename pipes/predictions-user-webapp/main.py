from flask import Flask, request, render_template, redirect, url_for
from bigquery_predictions import fetch_bq_predictions
from formatter import format_data

# Create Flask WSGI application instance.
app = Flask(__name__)

@app.route('/', methods=['GET'])
def web_page():

    table_bool = False

    if 'show_table' in request.args:
        table_bool = True

        df = fetch_bq_predictions()

        df = format_data(df)

        column_names = ['predicted_temp', 'data_dt', 'prediction_dt', 'timeframe_start', 'timeframe_end']

        return render_template("index.html", column_names=column_names, row_data=list(df.values.tolist()),
                            link_column="df index", zip=zip, table_bool=table_bool)

    return render_template("index.html", table_bool=table_bool)

@app.route('/clear_table', methods=['GET'])
def clear_table():
    # Redirect to the base URL, which clears the table (since no 'show_table' param will be present)
    return redirect(url_for('web_page'))

if __name__ == '__main__':
    # Run the application on port 8080.
    app.run(host='0.0.0.0', port=8080)