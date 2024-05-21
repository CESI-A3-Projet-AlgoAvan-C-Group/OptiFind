# This document contains the backend code for the application
# It is a Python file that will work similary to the future flask app
# It will contain simples classes and functions to test the GeoJSON library

# This project will use points (delivery) as the entry data
# And will return a path (route) to be followed by the delivery person

import geojson
import json

# This class will be used to represent the delivery points
class DeliveryPoint:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    @property
    def __geo_interface__(self):
        return {
            "type": "Point",
            "coordinates": (self.x, self.y)
        }
    
    def __str__(self):
        return f"DeliveryPoint: {self.__geo_interface__}"
    
    def __repr__(self):
        return self.__str__()
    
# This class will be used to represent the route to be followed by the delivery person
class Route:
    def __init__(self, points):
        self.points = points
    
    @property
    def __geo_interface__(self):
        return {
            "type": "LineString",
            "coordinates": [(point.x, point.y) for point in self.points]
        }
    
    def __str__(self):
        return f"Route: {self.__geo_interface__}"
    
    def __repr__(self):
        return self.__str__()
    
# This function will be used to calculate the route to be followed by the delivery person
def calculate_route(delivery_points):
    return Route(delivery_points)

# This function will be used to write the route to a GeoJSON file
def write_route_to_geojson(route, file_path):
    feature = geojson.Feature(geometry=route.__geo_interface__)
    feature_collection = geojson.FeatureCollection([feature])
    with open(file_path, 'w') as file:
        json.dump(feature_collection, file)

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
    test_main('data.geojson', 'route.geojson')