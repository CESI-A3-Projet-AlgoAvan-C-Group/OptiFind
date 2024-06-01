import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
import json
import random
import math
import numpy as np
import pandas as pd
import pulp
import itertools
import matplotlib.pyplot as plt
import csv

from src.package_handling import *
from src.package_delivery import *

# Haversine distance function
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371.0  # Radius of Earth in kilometers
    distance = c * r * 1000  # Convert to meters
    return distance

def calculate_packages_center(packages):
    if not packages:
        return 48.866667, 2.333333
    total_latitude = sum(package.latitude for package in packages)
    total_longitude = sum(package.longitude for package in packages)
    count = len(packages)
    return total_latitude / count, total_longitude / count

def extract_stats(vehicles):
    stats = {
        'num_packages_delivered': 0,
        'num_packages_not_delivered': 0,
        'max_num_packages_delivered': 0,
        'num_vehicles_used': len(vehicles),
        'total_distance': 0,
        'min_distance': float('inf'),
        'max_distance': 0
    }

    depot_latitude, depot_longitude = 48.866667, 2.333333

    for vehicle in vehicles:
        num_packages = len(vehicle.packages)
        remaining_capacity = vehicle.remaining_capacity
        remaining_volume = vehicle.remaining_volume
        
        package_center_latitude, package_center_longitude = calculate_packages_center(vehicle.packages)
        distance = haversine(depot_latitude, depot_longitude, package_center_latitude, package_center_longitude)
        
        stats['total_distance'] += distance
        if num_packages > stats['max_num_packages_delivered']:
            stats['max_num_packages_delivered'] = num_packages
        if distance < stats['min_distance']:
            stats['min_distance'] = distance
        if distance > stats['max_distance']:
            stats['max_distance'] = distance
        stats['num_packages_delivered'] += num_packages
        stats['num_packages_not_delivered'] += remaining_capacity + remaining_volume

    if stats['num_vehicles_used'] > 0:
        stats['average_distance'] = stats['total_distance'] / stats['num_vehicles_used']
    else:
        stats['average_distance'] = 0

    return stats

def generate_instance(num_packages):
    return {
        'startCity': '',
        'truckGroups': [
            {
                'id': 1,
                'name': 'truck_1',
                'quantity': '21',
                'volume': '20',
                'weight': '5',
                'truckType': 'classic'
            }
        ],
        'packageGroups': [
            {
                'id': 1,
                'name': 'package_1',
                'quantity': str(num_packages),
                'volume': str(random.uniform(0.01, 1.0)),
                'weight': str(random.uniform(0.01, 10.0)),
                'truckType': 'classic'
            }
        ],
        'mapData': None
    }

def run_heuristic_algorithm(data):
    vehicles = extract_vehicles(data['truckGroups'])
    packages = extract_packages_for_paths(data['mapData'])
    vehicles_allocated, packages_left = best_fit_decreasing_score(packages=packages, vehicles=vehicles)
    package = Package(0, 0, 0, 48.866667, 2.333333, 'Paris')
    for vehicle in vehicles_allocated:
        vehicle.add_package(package)
    vehicles_reorganized = reorganize_vehicles(vehicles_allocated, num_cores=1)

    stats = extract_stats(vehicles_reorganized)
    return stats, vehicles_reorganized

def run_mathematical_model(df, vehicle_count, vehicle_capacity):
    customer_count = len(df)
    
    # Calculate distance matrix using Haversine function
    def _distance_calculator(_df):
        _distance_result = np.zeros((len(_df), len(_df)))
        for i in range(len(_df)):
            for j in range(len(_df)):
                if i != j:
                    _distance_result[i][j] = haversine(_df['latitude'][i], _df['longitude'][i],
                                                       _df['latitude'][j], _df['longitude'][j])
        return _distance_result

    distance = _distance_calculator(df)

    # Problem definition
    problem = pulp.LpProblem("CVRP", pulp.LpMinimize)

    # Decision variables
    x = [[[pulp.LpVariable(f"x_{i}_{j}_{k}", cat="Binary") if i != j else None for k in range(vehicle_count)]
          for j in range(customer_count)] for i in range(customer_count)]

    # Objective function
    problem += pulp.lpSum(distance[i][j] * x[i][j][k] if i != j else 0
                          for k in range(vehicle_count)
                          for j in range(customer_count)
                          for i in range(customer_count))

    # Constraints
    # Each customer must be visited exactly once
    for j in range(1, customer_count):
        problem += pulp.lpSum(x[i][j][k] if i != j else 0 for i in range(customer_count) for k in range(vehicle_count)) == 1

    # Ensure that the vehicle enters and leaves each vertex exactly once
    for k in range(vehicle_count):
        for j in range(customer_count):
            problem += (pulp.lpSum(x[i][j][k] if i != j else 0 for i in range(customer_count)) ==
                        pulp.lpSum(x[j][i][k] if j != i else 0 for i in range(customer_count)))

    # Vehicle capacity constraints
    for k in range(vehicle_count):
        problem += pulp.lpSum(df['demand'][j] * x[i][j][k] if i != j else 0
                              for i in range(customer_count) for j in range(customer_count)) <= vehicle_capacity

    # Each tour must start and end at the depot
    for k in range(vehicle_count):
        problem += pulp.lpSum(x[0][j][k] for j in range(1, customer_count)) == 1
        problem += pulp.lpSum(x[i][0][k] for i in range(1, customer_count)) == 1

    # Subtour elimination constraints
    subtours = []
    for i in range(2, customer_count):
        subtours += itertools.combinations(range(1, customer_count), i)

    for s in subtours:
        for k in range(vehicle_count):
            problem += pulp.lpSum(x[i][j][k] if i != j else 0 for i, j in itertools.permutations(s, 2)) <= len(s) - 1

    # Solve the problem
    problem.solve()

    # Extract results
    if pulp.LpStatus[problem.status] == 'Optimal':
        total_distance = pulp.value(problem.objective)
        routes = {k: [] for k in range(vehicle_count)}
        for k in range(vehicle_count):
            for i in range(customer_count):
                for j in range(customer_count):
                    if i != j and pulp.value(x[i][j][k]) == 1:
                        routes[k].append((i, j))
        return total_distance, routes
    else:
        return None, None

def compare_algorithms(num_tests, num_packages, vehicle_count, vehicle_capacity):
    results = []

    for _ in range(num_tests):
        data = generate_instance(num_packages)
        
        # Extract package data for heuristic algorithm
        packages = extract_packages_with_random_city(data['packageGroups'])
        features = create_features_from_pkg(packages)
        packages_geojson = {
            "type": "FeatureCollection",
            "features": features
        }
        data['mapData'] = packages_geojson
        
        # Extract customer data for mathematical model
        package_data = [
            (pkg.latitude, pkg.longitude, pkg.weight)
            for pkg in packages
        ]
        df = pd.DataFrame(package_data, columns=['latitude', 'longitude', 'demand'])
        df.loc[len(df)] = [48.866667, 2.333333, 0]  # Add depot
        
        # Run heuristic algorithm
        heuristic_stats, heuristic_vehicles = run_heuristic_algorithm(data)
        
        # Run mathematical model
        model_distance, model_routes = run_mathematical_model(df, vehicle_count, vehicle_capacity)
        
        # Collect results
        heuristic_stats['model_total_distance'] = model_distance if model_distance is not None else float('inf')
        results.append(heuristic_stats)
        
    # Write results to CSV
    keys = results[0].keys()
    with open('algorithm_comparison_results.csv', 'w', newline='') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(results)

    # Generate comparison graphs
    generate_comparison_graphs(results)

def generate_comparison_graphs(results):
    num_vehicles_used = [result['num_vehicles_used'] for result in results]
    total_distances = [result['total_distance'] for result in results]
    model_total_distances = [result['model_total_distance'] for result in results]

    plt.figure(figsize=(12, 6))

    # Plot total distances comparison
    plt.subplot(1, 2, 1)
    plt.plot(total_distances, label='Heuristic Total Distance')
    plt.plot(model_total_distances, label='Model Total Distance')
    plt.xlabel('Test Instance')
    plt.ylabel('Total Distance')
    plt.legend()
    plt.title('Total Distance Comparison')

    # Plot number of vehicles used comparison
    plt.subplot(1, 2, 2)
    plt.plot(num_vehicles_used, label='Heuristic Number of Vehicles Used')
    plt.xlabel('Test Instance')
    plt.ylabel('Number of Vehicles Used')
    plt.legend()
    plt.title('Number of Vehicles Used Comparison')

    plt.tight_layout()
    plt.savefig('comparison_graphs.png')
    plt.show()

if __name__ == '__main__':
    num_tests = 10
    num_packages = 20
    vehicle_count = 4
    vehicle_capacity = 50
    compare_algorithms(num_tests, num_packages, vehicle_count, vehicle_capacity)
