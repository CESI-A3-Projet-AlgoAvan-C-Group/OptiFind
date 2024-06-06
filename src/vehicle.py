PARIS_LAT, PARIS_LON = 48.8566, 2.3522

class Vehicle:
    def __init__(self, vehicle_id, capacity, volume, vehicle_type):
        self.id = vehicle_id
        self.capacity = capacity
        self.remaining_capacity = capacity
        self.volume = volume
        self.remaining_volume = volume
        self.packages = []
        self.type = vehicle_type

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

    def calculate_distances_between_packages(self):
        distances = []
        for i in range(len(self.packages) - 1):
            distance = self.packages[i].calculate_distance(
                (self.packages[i + 1].latitude, self.packages[i + 1].longitude)
            )
            distances.append(distance)
        return sum(distances)

    def calculate_packages_center(self):
        if not self.packages:
            return PARIS_LAT, PARIS_LON
        total_latitude = sum(package.latitude for package in self.packages)
        total_longitude = sum(package.longitude for package in self.packages)
        count = len(self.packages)
        return [total_latitude / count, total_longitude / count]