from src.vehicle_manager import Vehicle, Package
from src.ant_colony import ant_colony

def reorganize_vehicles(vehicles):
    """
        Reorganize the vehicles to have a better distribution of packages

        Args:
        vehicles (list of Vehicle): List of Vehicle objects with their packages (Vehicle.packages).

        Returns:
        vehicles (list of Vehicle): List of Vehicle objects with their packages in the order they should be visited.
    """
    for vehicle in vehicles:
        if len(vehicle.packages) == 0:
            continue

        algorithm = "ant_colony"
        # Choose the algo
        algorithms(algorithm, vehicle)

    return vehicles

def algorithms(algorithm, vehicle):
    if algorithm == "ant_colony":
        ant_colony(vehicle)
    else:
        raise ValueError(f"Invalid algorithm: {algorithm}") 