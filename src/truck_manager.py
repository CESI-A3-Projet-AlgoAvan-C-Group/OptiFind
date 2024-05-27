def first_fit(package_weights, vehicle_capacities):

    remaining_capacities = vehicle_capacities[:]
    # [:] permet de faire une copie superficielle
    vehicles = [[] for _ in vehicle_capacities]
    # permet de creer une liste contenant une liste de vehicules ou les colis seront stockés

    for weight in package_weights:
        placed = False
        for i in range(len(remaining_capacities)):
            if remaining_capacities[i] >= weight:
                vehicles[i].append(weight)
                remaining_capacities[i] -= weight
                placed = True
                break

        if not placed:
            print(f"Erreur: Aucun véhicule ne peut contenir le colis ce colis de ({weight})")
            return None

    return vehicles
