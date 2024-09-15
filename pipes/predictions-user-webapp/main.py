from flask import Flask, request, render_template

# Create Flask WSGI application instance.
app = Flask(__name__)

@app.route('/', methods=['GET'])
def web_page():

    

    return render_template('index.html', message='Hello, World!')

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form['name']
    return f'Hello, {name}!'

if __name__ == '__main__':
    # Run the application on port 8080.
    app.run(host='0.0.0.0', port=8080)