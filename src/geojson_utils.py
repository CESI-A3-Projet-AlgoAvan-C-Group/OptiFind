import json
from delivery import Delivery

def create_geojson(paths_distances, file_path):
    """Create a GeoJSON file from the TSP paths."""
    features = []

    for i, (path, distance) in enumerate(paths_distances):
        if path:
            coordinates = [delivery.coordinates for delivery in path]
            feature = {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": coordinates
                },
                "properties": {
                    "cluster": i + 1,
                    "distance": distance
                }
            }
            features.append(feature)

    geojson = {
        "type": "FeatureCollection",
        "features": features
    }

    with open(file_path, 'w') as f:
        json.dump(geojson, f, indent=2)

def read_geojson(file_path):
    """Read cities data from a GeoJSON file."""
    with open(file_path, 'r') as f:
        data = json.load(f)
        
    cities = []
    for feature in data['features']:
        name = feature['properties']['delivery_address']
        coordinates = feature['geometry']['coordinates']
        is_start = feature['properties']['isStartingPoint']
        cities.append(Delivery(name, coordinates, is_start))
    
    return cities