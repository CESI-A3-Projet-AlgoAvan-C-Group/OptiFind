from src.vehicle_manager import Vehicle, Package, best_fit_decreasing_score
import geopandas as gpd
import random
import json


def create_features_from_pkg(packages):
    features = []

    for package in packages:
        package_feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [package.longitude, package.latitude]
            },
            "properties": {
                "package_id": package.id,
                "weight": package.weight,
                "volume": package.volume,
                "city": package.city,
                "truckType": package.type
            }
        }

        features.append(package_feature)

    return features


def extract_vehicles(truckGroups):
    vehicles = []
    for truck_index, truck in enumerate(truckGroups):
        print(truck)
        for i in range(int(truck['quantity'])):
            vehicle_id = (truck_index + 1) * 10000 + i + 1
            vehicle = Vehicle(
                vehicle_id=vehicle_id,
                capacity=float(truck['weight']),
                volume=float(truck['volume']),
                vehicle_type=str(truck['truckType']))
            vehicles.append(vehicle)

    return vehicles


def get_random_city(communes):
    random_number = random.randrange(0, len(communes))

    return communes.iloc[random_number]


def extract_packages_for_paths(mapData):
    packages = []
    for feature in mapData['features']:
        properties = feature['properties']
        geometry = feature['geometry']
        package = Package(
            package_id=properties['package_id'],
            weight=float(properties['weight']),
            volume=float(properties['volume']),
            latitude=geometry['coordinates'][1],
            longitude=geometry['coordinates'][0],
            city=properties['city'],
            package_type=str(properties['truckType'])
        )
        packages.append(package)
    return packages


def extract_packages_with_random_city(packageGroups):
    packages = []
    communes = gpd.read_file('../assets/data/centre_communes.geojson')

    for pkg_index, pkg in enumerate(packageGroups):
        for i in range(int(pkg['quantity'])):
            ville = get_random_city(communes)
            communes = communes.drop(ville.name)
            package_id = (pkg_index + 1) * 100000 + i + 1
            package = Package(
                package_id=package_id,
                weight=float(pkg['weight']),
                volume=float(pkg['volume']),
                latitude=ville.geometry.y,
                longitude=ville.geometry.x,
                city=ville.nom_officiel,
                package_type=str(pkg['truckType'])
            )

            packages.append(package)

    return packages


def find_start_city(cityname):
    cities = gpd.read_file('../assets/data/centre_communes.geojson')
    city = cities[cities.nom_officiel == cityname]
    return city if not city.empty else cities[cities.nom_officiel == 'Paris']