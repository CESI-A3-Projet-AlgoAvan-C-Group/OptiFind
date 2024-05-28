import os
import json
import csv
import argparse
os.environ["LOKY_MAX_CPU_COUNT"] = "4"  # Define the maximum number of CPU cores to use for parallel processing

from delivery_clusterer import DeliveryClusterer
from geojson_utils import create_geojson, read_geojson

import csv

def run_tests(input_file):
    # This function is used to test the code locally
    packages = read_geojson(input_file)

    with open('results.csv', 'w', newline='') as csvfile:
        fieldnames = ['Number of clusters', 'Average distance (TSP)', 'Max distance (TSP)', 'Average distance (Antoine)', 'Max distance (Antoine)']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()

        # Test The Delivery distance for both algorithms with different number of clusters
        for n_trucks in range(2, 8):
            delivery_clusterer = DeliveryClusterer(packages, n_trucks)
            delivery_clusterer.cluster_deliveries()

            # Solve TSP for each cluster
            paths_distances_tsp = delivery_clusterer.solve_paths("tsp")
            paths_distances_antoine = delivery_clusterer.solve_paths("antoine")

            # Calculate average and max distance for TSP algorithm
            avg_distance_tsp = sum(distance for _, distance in paths_distances_tsp) / len(paths_distances_tsp)
            max_distance_tsp = max(distance for _, distance in paths_distances_tsp)

            # Calculate average and max distance for Antoine's algorithm
            avg_distance_antoine = sum(distance for _, distance in paths_distances_antoine) / len(paths_distances_antoine)
            max_distance_antoine = max(distance for _, distance in paths_distances_antoine)

            writer.writerow({'Number of clusters': n_trucks, 'Average distance (TSP)': avg_distance_tsp, 'Max distance (TSP)': max_distance_tsp, 'Average distance (Antoine)': avg_distance_antoine, 'Max distance (Antoine)': max_distance_antoine})

def main(input_file, output_file, n_trucks=5):
    # Read packages data from GeoJSON file
    packages = read_geojson(input_file)

    # Cluster the packages
    delivery_clusterer = DeliveryClusterer(packages, n_trucks)
    delivery_clusterer.cluster_deliveries()

    # Solve TSP for each cluster
    paths_distances = delivery_clusterer.solve_paths("antoine")

    # Create GeoJSON file with TSP paths
    create_geojson(paths_distances, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cluster packages and solve TSP paths, then output to GeoJSON.')
    parser.add_argument('input_file', type=str, help='Path to the input GeoJSON file')
    parser.add_argument('output_file', type=str, help='Path to the output GeoJSON file')
    parser.add_argument('--clusters', type=int, default=5, help='Number of clusters (default: 5)')
    parser.add_argument('--test', action='store_true', help='Run tests')

    args = parser.parse_args()

    if args.test:
        run_tests(args.input_file)
    else:
        main(args.input_file, args.output_file, args.clusters)