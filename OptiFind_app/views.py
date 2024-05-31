from flask import Flask
from flask_cors import CORS
from flask import send_from_directory
from src.package_handling import *
from src.package_delivery import *

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

@app.route('/get_packages', methods=['POST'])
def get_packages():
    data = request.json  # data from the client

    packages = extract_packages_with_random_city(data['packageGroups'])
    features = create_features_from_pkg(packages)

    packages_geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    return packages_geojson


@app.route('/get_paths', methods=['POST'])
def handle_json():
    data = request.json # data from the client

    vehicles = extract_vehicles(data['truckGroups'])
    packages = extract_packages_for_paths(data['mapData'])

    vehicles_allocated, packages_left = best_fit_decreasing_score(packages=packages, vehicles=vehicles)

    vehicles_reorganized = reorganize_vehicles(vehicles_allocated, start_delivery=packages[0])

    return data