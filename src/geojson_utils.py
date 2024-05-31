import json

def generate_geojson_vehicles(vehicles):
    features = []
    for vehicle in vehicles:
        line_string = {
            "type": "LineString",
            "coordinates": [[package.longitude, package.latitude] for package in vehicle.packages]
        }
        feature = {
            "type": "Feature",
            "properties": {
                "id": vehicle.id,
                "capacity": vehicle.capacity,
                "remaining_capacity": vehicle.remaining_capacity,
                "volume": vehicle.volume,
                "remaining_volume": vehicle.remaining_volume,
                "packages": [package.id for package in vehicle.packages]
            },
            "geometry": line_string
        }
        features.append(feature)
    feature_collection = {
        "type": "FeatureCollection",
        "features": features
    }
    return json.dumps(feature_collection)

def generate_geojson_vehicle(vehicle):
    line_string = {
        "type": "LineString",
        "coordinates": [[package.longitude, package.latitude] for package in vehicle.packages]
    }
    feature = {
        "type": "Feature",
        "properties": {
            "id": vehicle.id,
            "capacity": vehicle.capacity,
            "remaining_capacity": vehicle.remaining_capacity,
            "volume": vehicle.volume,
            "remaining_volume": vehicle.remaining_volume,
            "packages": [package.id for package in vehicle.packages]
        },
        "geometry": line_string
    }
    feature_collection = {
        "type": "FeatureCollection",
        "features": [feature]
    }
    return json.dumps(feature_collection)

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