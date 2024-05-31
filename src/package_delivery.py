from src.vehicle_manager import Vehicle, Package

def reorganize_vehicles(vehicles, start_delivery):
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

        algorithm = "antoine"
        # Choose the algo
        algorithms(algorithm, vehicle, start_delivery)

    return vehicles

def antoine_algorithm(vehicle, start_delivery):
    # Reimplement the algorithm to use the new Vehicle class
    # Create a list of clusters, each containing a single package
    clusters = [[package] for package in vehicle.packages]

    # Merge the two closest clusters until only one remains
    while len(clusters) > 1:
        closest_clusters = None
        case_closest_clusters = None
        min_distance = float('inf')
        for i in range(len(clusters)):
            for j in range(i + 1, len(clusters)):
                case_1 = clusters[i][0].calculate_distance(clusters[j][0])
                case_2 = clusters[i][-1].calculate_distance(clusters[j][0])
                case_3 = clusters[i][0].calculate_distance(clusters[j][-1])
                case_4 = clusters[i][-1].calculate_distance(clusters[j][-1])
                distances = [case_1, case_2, case_3, case_4]
                for distance in distances:
                    if distance < min_distance:
                        min_distance = distance
                        closest_clusters = (i, j)
                        case_closest_clusters = distances.index(distance)
        i, j = closest_clusters
        if case_closest_clusters == 0:
            clusters[i].extend(clusters[j])
        elif case_closest_clusters == 1:
            clusters[i].extend(clusters[j][::-1])
        elif case_closest_clusters == 2:
            clusters[i] = clusters[j] + clusters[i]
        elif case_closest_clusters == 3:
            clusters[i] = clusters[j][::-1] + clusters[i]
        clusters.pop(j)

    # Now we have the path of packages in the order they should be visited
    vehicle.packages = clusters[0]

def algorithms(algorithm, vehicle, start_delivery):
    if algorithm == "antoine":
        antoine_algorithm(vehicle, start_delivery)
    else:
        raise ValueError(f"Invalid algorithm: {algorithm}")