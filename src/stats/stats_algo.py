import sys
import os
import json
import random

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from src.package_handling import *
from src.package_delivery import *

def generate_instances(num_tests, num_packages):

    for i in range(num_tests):
        data = generate_instance(num_packages)
        packages = extract_packages_with_random_city(data['packageGroups'])
        features = create_features_from_pkg(packages)

        packages_geojson = {
            "type": "FeatureCollection",
            "features": features
        }

        data['mapData'] = packages_geojson
        
        # Now we have the instance, we can test the algorithms
    

def generate_instance(num_packages):
    return {
        'startCity': '',
        'truckGroups': [
            {
                'id': 1,
                'name': 'truck_1',
                'quantity': str(random.randint(20, 50)),
                'volume': str(random.randint(20, 23)),
                'weight': str(random.randint(2, 5)),
                'truckType': 'classic'
            },
            {
                'id': 2,
                'name': 'truck_2',
                'quantity': str(random.randint(20, 50)),
                'volume': str(random.randint(80, 100)),
                'weight': str(random.randint(10, 20)),
                'truckType': 'classic'
            }
        ],
        'packageGroups': [
            {
                'id': 1,
                'name': 'package_1',
                'quantity': str(round(num_packages / 2)),
                'volume': str(random.uniform(0.01, 1.0)),
                'weight': str(random.uniform(0.01, 10.0)),
                'truckType': 'classic'
            },
            {
                'id': 2,
                'name': 'package_2',
                'quantity': str(round(num_packages / 2)),
                'volume': str(random.uniform(0.1, 1.0)),
                'weight': str(random.uniform(1.0, 10.0)),
                'truckType': 'classic'
            }
        ],
        'mapData': None
    }

def instance_generator():
    generate_instances(10000, 10)
    generate_instances(10000, 20)
    generate_instances(1000, 50)
    generate_instances(50, 1000)
    generate_instances(20, 10000)

def handle_json(data, starting_point='Paris'): # Latitude : 48.866667. Longitude : 2.333333
    
    vehicles = extract_vehicles(data['truckGroups'])
    packages = extract_packages_for_paths(data['mapData'])
    vehicles_allocated, packages_left = best_fit_decreasing_score(packages=packages, vehicles=vehicles)
    package = Package(0, 0, 0, 48.866667, 2.333333, 'Paris')
    for vehicle in vehicles_allocated:
        vehicle.add_package(package)
    vehicles_reorganized = reorganize_vehicles(vehicles_allocated, num_cores=4)

def main():
    instance_generator()