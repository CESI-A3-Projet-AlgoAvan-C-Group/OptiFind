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