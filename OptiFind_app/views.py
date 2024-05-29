from flask import Flask
from flask_cors import CORS
from flask import send_from_directory
from src.vehicle_manager import Vehicle, Package, best_fit_decreasing_score
import geopandas as gpd
import random
import json

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

    vehicles = extract_vehicles(data['truckGroups'])
    packages, features = extract_packages(data['packageGroups'])

    packages_geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open('../assets/data/packages.geojson', 'w') as outfile:
        json.dump(packages_geojson, outfile)

    return packages_geojson

def extract_vehicles(truckGroups):
    vehicles = []
    for truck_index, truck in enumerate(truckGroups):
        for i in range(int(truck['quantity'])):
            vehicle_id = (truck_index+1) * 10000 + i + 1
            vehicle = Vehicle(
                vehicle_id=vehicle_id,
                capacity=float(truck['weight']),
                volume=float(truck['volume']))
            vehicles.append(vehicle)

    return vehicles

def extract_packages(packageGroups):
    communes = gpd.read_file('../assets/data/centre_communes.geojson')
    packages = []
    features = []

    for pkg_index, pkg in enumerate(packageGroups):
        for i in range(int(pkg['quantity'])):
            random_number = random.randrange(0, len(communes))
            ville = communes.iloc[random_number]
            print(ville)
            package_id = (pkg_index+1) * 10000 + i + 1
            package = Package(
                package_id= package_id,
                weight=float(pkg['weight']),
                volume=float(pkg['volume']),
                latitude=ville.geometry.y,
                longitude=ville.geometry.x,
                city=ville.nom_officiel)
            packages.append(package)

            package_feature = {
                "type": "Feature",
                "geometry": {
                    "type": "Point",
                    "coordinates": [package.longitude, package.latitude]
                },
                "properties": {
                    "package_id": package.id,
                    "weight": package.weight,
                    "volume": package.volume,
                    "city": package.city
                }
            }

            features.append(package_feature)

    return packages, features