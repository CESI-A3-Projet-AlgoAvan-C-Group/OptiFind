from flask import Flask
from flask_cors import CORS
from flask import send_from_directory

app = Flask(__name__)
CORS(app)

@app.route("/<path:path>")
def home(path):
    return send_from_directory('webview', path)

@app.route("/")
def index():
    return send_from_directory('webview', 'index.html')

from flask import Flask, request
# ...

@app.route('/get_paths', methods=['POST'])
def handle_json():
    data = request.json # data from the client
    with open('../assets/data/route.geojson', 'r') as outfile:
        return outfile.read() # return the data to the client
