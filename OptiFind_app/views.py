import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask
from flask_cors import CORS
from flask import send_from_directory
from src.package_handling import *
from src.package_delivery import *
from flask_socketio import SocketIO
from flask import request
from src.geojson_utils import *

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)


@app.route("/<path:path>")
def home(path):
    return send_from_directory('webview', path)


@app.route("/")
def index():
    return send_from_directory('webview', 'index.html')


@app.route('/get_paths', methods=['POST'])
def get_packages():
    data = request.json  # data from the client

    if data['mapData'] is None:
        packages = extract_packages_with_random_city(data['packageGroups'])
        features = create_features_from_pkg(packages)

        packages_geojson = {
            "type": "FeatureCollection",
            "features": features
        }


        socketio.emit('newLayerPoints', packages_geojson)
        data['mapData'] = packages_geojson
        handle_json(data)
    else:
        handle_json(data)

    return 'Packages received'


def handle_json(data, starting_point='Paris'): # Latitude : 48.866667. Longitude : 2.333333
    vehicles = extract_vehicles(data['truckGroups'])
    packages = extract_packages_for_paths(data['mapData'])

    vehicles_allocated, packages_left = best_fit_decreasing_score(packages=packages, vehicles=vehicles)

    # Add a package to the start of the delivery at Paris
    package = Package(0, 0, 0, 48.866667, 2.333333, 'Paris')
    for vehicle in vehicles_allocated:
        vehicle.add_package(package)

    vehicles_reorganized = reorganize_vehicles(vehicles_allocated)

    # vehicles_geojson = generate_geojson_vehicles(vehicles_reorganized)
    # socketio.emit('newLayerPoints', vehicles_geojson)

    for vehicle in vehicles_reorganized:
        if len(vehicle.packages) == 0:
            continue
        vehicle_geojson = generate_geojson_vehicle(vehicle)
        socketio.emit('newLayerLines', vehicle_geojson)
    return 'Paths received'


if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000)
