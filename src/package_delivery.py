from concurrent.futures import ProcessPoolExecutor

from src.geojson_utils import read_geojson
from src.vehicle_manager import Vehicle, Package
from src.ant_colony import ant_colony
import copy

def reorganize_vehicles(vehicles, num_cores):
    """
        Reorganize the vehicles to have a better distribution of packages

        Args:
        vehicles (list of Vehicle): List of Vehicle objects with their packages (Vehicle.packages).

        Returns:
        vehicles (list of Vehicle): List of Vehicle objects with their packages in the order they should be visited.
    """
    algorithm = "ant_colony"
    results = []
    with ProcessPoolExecutor(max_workers=num_cores) as executor:
        futures = []
        for vehicle in vehicles:
            if len(vehicle.packages) == 0:
                continue
            # Choose the algo
            vehicle_copy = copy.deepcopy(vehicle)
            futures.append(executor.submit(algorithms, algorithm, vehicle_copy))
        for future in futures:
            results.append(future.result())
    return results

def algorithms(algorithm, vehicle):
    try:
        if algorithm == "ant_colony":
            return ant_colony(vehicle)
        else:
            raise ValueError(f"Invalid algorithm: {algorithm}")
    except Exception as e:
        print(f"An error occurred: {e}")