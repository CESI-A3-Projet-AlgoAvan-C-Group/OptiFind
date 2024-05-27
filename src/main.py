import os
import json
import argparse
os.environ["LOKY_MAX_CPU_COUNT"] = "4"  # Define the maximum number of CPU cores to use for parallel processing

from delivery_clusterer import DeliveryClusterer
from geojson_utils import create_geojson, read_geojson

def main(input_file, output_file, n_clusters=5):
    # Read cities data from GeoJSON file
    cities = read_geojson(input_file)

    # Cluster the cities
    delivery_clusterer = DeliveryClusterer(cities, n_clusters)
    delivery_clusterer.cluster_cities()

    # Solve TSP for each cluster
    paths_distances = delivery_clusterer.solve_paths()

    # Create GeoJSON file with TSP paths
    create_geojson(paths_distances, output_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Cluster cities and solve TSP paths, then output to GeoJSON.')
    parser.add_argument('input_file', type=str, help='Path to the input GeoJSON file')
    parser.add_argument('output_file', type=str, help='Path to the output GeoJSON file')
    parser.add_argument('--clusters', type=int, default=5, help='Number of clusters (default: 5)')

    args = parser.parse_args()
    main(args.input_file, args.output_file, args.clusters)