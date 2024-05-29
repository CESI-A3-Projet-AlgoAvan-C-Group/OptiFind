from math import radians, sin, cos, sqrt, atan2

class Vehicle:
    def __init__(self, vehicle_id, capacity, volume):
        self.id = vehicle_id
        self.capacity = capacity
        self.remaining_capacity = capacity
        self.volume = volume
        self.remaining_volume = volume
        self.packages = []

    def add_package(self, package):
        if self.remaining_capacity >= package.weight or self.remaining_volume >= package.volume:
            self.packages.append(package)
            self.remaining_capacity -= package.weight
            self.remaining_volume -= package.volume

    def remove_package(self, package):
        if package in self.packages:
            self.packages.remove(package)
            self.remaining_capacity += package.weight
            self.remaining_volume += package.volume

    def calculate_packages_center(self):
        if not self.packages:
            return 48.866667, 2.333333
        total_latitude = sum(package.latitude for package in self.packages)
        total_longitude = sum(package.longitude for package in self.packages)
        count = len(self.packages)
        return [total_latitude / count, total_longitude / count]


class Package:
    def __init__(self, package_id, weight, volume, latitude, longitude, city):
        self.id = package_id
        self.weight = weight
        self.volume = volume
        self.latitude = latitude
        self.longitude = longitude
        self.city= city

    def calculate_distance(self, reference_position):
        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(reference_position[0])
        lon2 = radians(reference_position[1])

        R = 6371.0

        dlat = abs(lat2 - lat1)
        dlon = abs(lon2 - lon1)

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c

        return distance


def calculate_score(package, vehicle, max_distance=500):

    center_position = vehicle.calculate_packages_center()
    distance = package.calculate_distance(center_position)

    if distance > max_distance and (len(vehicle.packages) != 0):
        return -1

    if distance > max_distance and (len(vehicle.packages) == 0):
        max_distance = distance

    score = ((package.weight / vehicle.remaining_capacity) + (package.volume / vehicle.remaining_volume) + ((1 - (distance / max_distance)) * 1.2))
    return score


def best_fit_decreasing_score(packages, vehicles):
    """
        Attribue les colis aux véhicules en utilisant le principe d'un algorithme BFD avec une fonction score.

        Args:
        packages (list of Package): Liste d'objets Package représentant les colis à distribuer.
        vehicles (list of Vehicle): Liste d'objets Vehicle représentant les véhicules disponibles.

        Returns:
        vehicles (list of Vehicle): Liste d'objets Vehicle avec leur colis (Vehicle.packages).
        packages_left (list of Package): Liste d'objets Package qui n'ont pas été distribués.
    """

    sorted_packages = sorted(packages, key=lambda x: (x.weight, x.volume), reverse=True)
    packages_left = []

    for package in sorted_packages:
        best_fit_vehicle = None
        best_score = float(0)

        for vehicle in vehicles:
            if vehicle.remaining_capacity >= package.weight and vehicle.remaining_volume >= package.volume:
                score = calculate_score(package, vehicle)
                if score > best_score:
                    best_score = score
                    best_fit_vehicle = vehicle

        if best_fit_vehicle is None:
            packages_left.append(package)
            continue

        best_fit_vehicle.add_package(package)

    return vehicles, packages_left

def best_fit_decreasing(packages, vehicles):
    """
        Attribue les colis aux véhicules en utilisant l'algorithme Best Fit Decreasing.

        Args:
        packages (list of Package): Liste d'objets Package représentant les colis à distribuer.
        vehicles (list of Vehicle): Liste d'objets Vehicle représentant les véhicules disponibles.

        Returns:
        vehicles (list of Vehicle): Liste d'objets Vehicle avec leur colis (Vehicle.packages).
        packages_left (list of Package): Liste d'objets Package qui n'ont pas été distribués.
    """

    sorted_packages = sorted(packages, key=lambda x: (x.weight, x.volume), reverse=True)
    packages_left = []

    for package in sorted_packages:
        best_fit_vehicle = None
        min_space_left = float('inf')
        min_volume_left = float('inf')

        for vehicle in vehicles:
            if vehicle.remaining_capacity >= package.weight and vehicle.remaining_volume >= package.volume:
                space_left = vehicle.remaining_capacity - package.weight
                volume_left = vehicle.remaining_volume - package.volume

                if space_left < min_space_left or (space_left == min_space_left and volume_left < min_volume_left):
                    best_fit_vehicle = vehicle
                    min_space_left = space_left
                    min_volume_left = volume_left

        if best_fit_vehicle is None:
            packages_left.append(package)
            continue

        best_fit_vehicle.add_package(package)

    return vehicles, packages_left