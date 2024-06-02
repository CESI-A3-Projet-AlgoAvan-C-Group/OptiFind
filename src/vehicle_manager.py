from math import radians, sin, cos, sqrt, atan2

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

    def calculate_packages_center(self):
        if not self.packages:
            return PARIS_LAT, PARIS_LON
        total_latitude = sum(package.latitude for package in self.packages)
        total_longitude = sum(package.longitude for package in self.packages)
        count = len(self.packages)
        return [total_latitude / count, total_longitude / count]


class Package:
    def __init__(self, package_id, weight, volume, latitude, longitude, city, package_type):
        self.id = package_id
        self.weight = weight
        self.volume = volume
        self.latitude = latitude
        self.longitude = longitude
        self.city = city
        self.type = package_type

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

def calculate_score(package, vehicle, max_distance=150):

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
            if (vehicle.remaining_capacity >= package.weight and vehicle.remaining_volume >= package.volume
                    and vehicle.type == package.type):
                score = calculate_score(package, vehicle)
                if score > best_score:
                    best_score = score
                    best_fit_vehicle = vehicle

        if best_fit_vehicle is None:
            packages_left.append(package)
            continue

        best_fit_vehicle.add_package(package)

    return vehicles, packages_left


def best_fit(packages, vehicles):
    """
        Attribue les colis aux véhicules en utilisant l'algorithme Best Fit Decreasing.

        Args:
        packages (list of Package): Liste d'objets Package représentant les colis à distribuer.
        vehicles (list of Vehicle): Liste d'objets Vehicle représentant les véhicules disponibles.

        Returns:
        vehicles (list of Vehicle): Liste d'objets Vehicle avec leur colis (Vehicle.packages).
        packages_left (list of Package): Liste d'objets Package qui n'ont pas été distribués.
    """

    packages_left = []

    for package in packages:
        best_fit_vehicle = None
        min_space_left = float('inf')
        min_volume_left = float('inf')

        for vehicle in vehicles:
            if (vehicle.remaining_capacity >= package.weight and vehicle.remaining_volume >= package.volume
                    and vehicle.type == package.type):
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


def first_fit(packages, vehicles):
    """
    Attribue les colis aux véhicules en utilisant l'algorithme First Fit.

    Args:
    packages (list of Package): Liste d'objets Package représentant les colis à distribuer.
    vehicles (list of Vehicle): Liste d'objets Vehicle représentant les véhicules disponibles.

    Returns:
    vehicles (list of Vehicle): Liste d'objets Vehicle avec leurs colis (Vehicle.packages).
    packages_left (list of Package): Liste d'objets Package qui n'ont pas été distribués.
    """

    packages_left = []

    sorted_vehicles = sorted(vehicles, key=lambda x: (x.capacity, x.volume), reverse=True)

    for package in packages:
        assigned = False
        for vehicle in sorted_vehicles:
            if (vehicle.remaining_capacity >= package.weight and vehicle.remaining_volume >= package.volume
                    and vehicle.type == package.type):
                vehicle.add_package(package)
                assigned = True
                break

        if not assigned:
            packages_left.append(package)

    return sorted_vehicles, packages_left

def assign_region(package, grid_rows, grid_cols, lat_min, lat_max, lon_min, lon_max):
    lat_step = (lat_max - lat_min) / grid_rows
    lon_step = (lon_max - lon_min) / grid_cols

    row = int((package.latitude - lat_min) / lat_step)
    col = int((package.longitude - lon_min) / lon_step)

    return row, col

def calculate_farthest_region(grid, paris_lat, paris_lon):
    max_distance = 0
    farthest_region = None

    for (row, col), packages in grid.items():
        if not packages:
            continue
        region_center = (sum(p.latitude for p in packages) / len(packages),
                         sum(p.longitude for p in packages) / len(packages))
        distance = Package("", 0, 0, *region_center, "").calculate_distance((paris_lat, paris_lon))
        if distance > max_distance:
            max_distance = distance
            farthest_region = (row, col)

    return farthest_region


def get_neighbors(region, grid_rows, grid_cols):
    row, col = region
    neighbors = []

    for d_row in [-1, 0, 1]:
        for d_col in [-1, 0, 1]:
            if d_row == 0 and d_col == 0:
                continue
            n_row, n_col = row + d_row, col + d_col
            if 0 <= n_row < grid_rows and 0 <= n_col < grid_cols:
                neighbors.append((n_row, n_col))

    return neighbors


def generate_snail_pattern(start_row, start_col, grid_rows, grid_cols):
    snail_pattern = []
    visited = set()
    directions = [(0, -1), (-1, 0), (0, 1), (1, 0)]  # Left, Up, Right, Down
    direction_index = 0

    row, col = start_row, start_col

    for _ in range(grid_rows * grid_cols):
        if (row, col) in visited or not (0 <= row < grid_rows) or not (0 <= col < grid_cols):
            break
        snail_pattern.append((row, col))
        visited.add((row, col))

        # Calculate next position
        next_row, next_col = row + directions[direction_index][0], col + directions[direction_index][1]

        # Change direction if next position is out of bounds or already visited
        if not (0 <= next_row < grid_rows) or not (0 <= next_col < grid_cols) or (next_row, next_col) in visited:
            direction_index = (direction_index + 1) % 4
            next_row, next_col = row + directions[direction_index][0], col + directions[direction_index][1]

        row, col = next_row, next_col

    return snail_pattern

def distribute_packages(packages, vehicles, lat_min = 41.0, lat_max = 51.0, lon_min = -5.0, lon_max = 9.0, grid_rows = 10, grid_cols = 10):
    grid = {(i, j): [] for i in range(grid_rows) for j in range(grid_cols)}

    for package in packages:
        region = assign_region(package, grid_rows, grid_cols, lat_min, lat_max, lon_min, lon_max)
        if region in grid:
            grid[region].append(package)

    print(grid_rows, grid_cols)
    snail_order = generate_snail_pattern(grid_rows-1, grid_cols-1, grid_rows, grid_cols)
    print(snail_order)
    leftover = []
    print(len(packages))
    for region in snail_order:
        packages_to_distribute = grid.pop(region, [])
        sorted_packages = sorted(leftover, key=lambda x: (x.weight, x.volume), reverse=True)
        sorted_packages.extend(sorted(packages_to_distribute, key=lambda x: (x.weight, x.volume), reverse=True))

        if sorted_packages:
            vehicles, leftover = first_fit(sorted_packages, vehicles)
        else:
            continue

    return vehicles, leftover