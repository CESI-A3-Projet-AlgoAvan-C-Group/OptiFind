import geojson
import json

from algorithm import calculate_route, write_route_to_geojson
from delivery_point import DeliveryPoint

# This function will be used to test the main functionalities of the application
def test_main(input_file_path, output_file_path):
    with open(input_file_path, 'r') as file:
        data = json.load(file)
        features = data['features']
        delivery_points = []
        for feature in features:
            if feature['geometry']['type'] == 'Point':
                delivery_points.append(DeliveryPoint(*feature['geometry']['coordinates']))
    route = calculate_route(delivery_points)
    write_route_to_geojson(route, output_file_path)

# Exemple d'utilisation
if __name__ == "__main__":
    test_main('assets/data/data.geojson', 'assets/data/route.geojson')