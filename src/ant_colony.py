import numpy as np

def ant_colony(vehicule):
    # Ant colony algorithm to resolve the TSP
    # The goal it to reoder the packages in the vehicle to have the shortest path, starting and ending at the same point

    # The packages are the nodes of the graph
    packages = vehicule.packages
    n = len(packages)
    
    # The distance between the packages are the edges of the graph
    distance_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            distance_matrix[i, j] = packages[i].calculate_distance([packages[j].latitude, packages[j].longitude])

    # Parameters
    n_ants = 10
    n_best = 2
    n_iterations = 100
    elitist_weight = 10
    decay = 0.95
    alpha = 1
    beta = 2

    # Pheromone matrix
    pheromone = np.ones((n, n))
    np.fill_diagonal(pheromone, 0)

    # Intensities
    epsilon = 1e-10
    intensity = 1 / (distance_matrix + epsilon)
    intensity[intensity == np.inf] = 0

    # Best path
    best_path = (np.inf, None)

    for it in range(n_iterations):
        # Initialize ants
        ants = np.zeros((n_ants, n+1)).astype(int)  # Increase the size by 1 to accommodate the return to the start
        for i in range(n_ants):
            current = np.random.randint(0, n)
            ants[i, 0] = current
            visited = set([current])
            for j in range(1, n):
                p = pheromone[current] ** alpha * intensity[current] ** beta
                p[[*visited]] = 0
                p = p / p.sum()
                next = np.random.choice(n, p=p)
                ants[i, j] = next
                visited.add(next)
                current = next
            ants[i, n] = ants[i, 0]  # Add the starting point at the end of the tour

        # Update pheromone
        for i in range(n_ants):
            path = ants[i]
            distance = sum(distance_matrix[path[k], path[k + 1]] for k in range(n))  # Calculate the distance including the return to the start
            if distance < best_path[0]:
                best_path = (distance, path)
            for k in range(n):  # Update the pheromone for the return to the start
                if distance != 0:
                    pheromone[path[k], path[(k + 1) % n]] += 1 / distance


        # Elitist update
        for k in range(n):
            if best_path[0] != 0:
                pheromone[best_path[1][k], best_path[1][(k + 1) % n]] += elitist_weight / best_path[0]
        
        # Evaporation
        pheromone *= decay

    # Reorder the packages
    new_order = [packages[i] for i in best_path[1]]
    vehicule.packages = new_order
    return vehicule