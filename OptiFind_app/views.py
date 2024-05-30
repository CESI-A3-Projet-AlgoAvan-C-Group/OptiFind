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

    return data


def create_features_from_pkg(packages):
    features = []

    for package in packages:
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

    return features


def extract_vehicles(truckGroups):
    vehicles = []
    for truck_index, truck in enumerate(truckGroups):
        print(truck)
        for i in range(int(truck['quantity'])):
            vehicle_id = (truck_index+1) * 10000 + i + 1
            vehicle = Vehicle(
                vehicle_id=vehicle_id,
                capacity=float(truck['weight']),
                volume=float(truck['volume']))
            vehicles.append(vehicle)

    return vehicles


def get_random_city(communes):
    random_number = random.randrange(0, len(communes))

    return communes.iloc[random_number]

def extract_packages_for_paths(mapData):
    packages = []
    for feature in mapData['features']:
        properties = feature['properties']
        geometry = feature['geometry']
        package = Package(
            package_id=properties['package_id'],
            weight=float(properties['weight']),
            volume=float(properties['volume']),
            latitude=geometry['coordinates'][1],
            longitude=geometry['coordinates'][0],
            city=properties['city']
        )
        packages.append(package)
    return packages

def extract_packages_with_random_city(packageGroups):
    packages = []
    communes = gpd.read_file('../assets/data/centre_communes.geojson')

    for pkg_index, pkg in enumerate(packageGroups):
        for i in range(int(pkg['quantity'])):
            ville = get_random_city(communes)
            package_id = (pkg_index+1) * 100000 + i + 1
            package = Package(
                package_id= package_id,
                weight=float(pkg['weight']),
                volume=float(pkg['volume']),
                latitude=ville.geometry.y,
                longitude=ville.geometry.x,
                city=ville.nom_officiel)

            packages.append(package)

    return packages