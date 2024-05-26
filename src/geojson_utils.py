import json
from city import City

def create_geojson(clusters, file_path):
    """Create a GeoJSON file from the clustered cities' TSP paths."""
    features = []

    for i, cluster in enumerate(clusters):
        start_city = next(city for city in cluster.cities if city.name == "Paris")
        path, distance = cluster.tsp_path(start_city)
        if path:
            coordinates = [city.coordinates for city in path]
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
        name = feature['properties']['city']
        coordinates = feature['geometry']['coordinates']
        is_start = feature['properties']['isStartingPoint']
        cities.append(City(name, coordinates, is_start))
    
    return cities