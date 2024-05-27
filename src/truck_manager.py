def best_fit_decreasing(package_weights, vehicle_capacities):

    sorted_weights = sorted(package_weights, reverse=True)
    remaining_capacities = vehicle_capacities[:] # [:] permet de faire une copie superficielle
    vehicles = [[] for _ in vehicle_capacities]
    packages_left = []

    for weight in sorted_weights:
        best_fit_index = -1
        min_space_left = float('inf')

        for i in range(len(remaining_capacities)):
            if remaining_capacities[i] >= weight and remaining_capacities[i] - weight < min_space_left:
                best_fit_index = i
                min_space_left = remaining_capacities[i] - weight

        if best_fit_index == -1:
            packages_left.append(weight)
            break

        vehicles[best_fit_index].append(weight)
        remaining_capacities[best_fit_index] -= weight

    return vehicles, packages_left