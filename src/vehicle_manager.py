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

class Package:
    def __init__(self, package_id, weight, volume, coordinate):
        self.id = package_id
        self.weight = weight
        self.volume = volume
        self.coordinate = coordinate

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