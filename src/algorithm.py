import geojson
import json

from routes import Route

# This function will be used to calculate the route to be followed by the delivery person
def calculate_route(delivery_points):
    return Route(delivery_points)

# This function will be used to write the route to a GeoJSON file
def write_route_to_geojson(route, file_path):
    feature = geojson.Feature(geometry=route.__geo_interface__)
    feature_collection = geojson.FeatureCollection([feature])
    with open(file_path, 'w') as file:
        json.dump(feature_collection, file)