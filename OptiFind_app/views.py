from flask import Flask
from flask_cors import CORS
from flask import send_from_directory

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return send_from_directory("webView", "index.html")