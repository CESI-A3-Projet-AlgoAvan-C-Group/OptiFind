from sklearn.cluster import KMeans
import numpy as np
from delivery import Delivery
from delivery_cluster import DeliveryPathFinder

class DeliveryClusterer:
    def __init__(self, deliveries, n_trucks):
        self.deliveries = deliveries
        self.n_trucks = n_trucks
        self.trucks = []

    def cluster_deliveries(self):
        coordinates = np.array([delivery.coordinates for delivery in self.deliveries])
        kmeans = KMeans(n_trucks=self.n_trucks, n_init=10)
        labels = kmeans.fit_predict(coordinates)
        
        self.trucks = [DeliveryPathFinder([]) for _ in range(self.n_trucks)]
        start_index = next(i for i, delivery in enumerate(self.deliveries) if delivery.is_start)
        
        # Ensure the starting delivery is in every cluster
        for cluster in self.trucks:
            cluster.deliveries.append(self.deliveries[start_index])
    
        for delivery, label in zip(self.deliveries, labels):
            if not delivery.is_start:  # The starting delivery is already added to all trucks
                self.trucks[label].deliveries.append(delivery)

    def solve_paths(self, algorithm):
        if algorithm == "tsp":
            return self.solve_tsp()
        elif algorithm == "antoine":
            return self.solve_antoine()
        else:
            raise ValueError(f"Invalid algorithm: {algorithm}")

    def solve_tsp(self):
        """Solve the TSP for each cluster and return the paths and distances."""
        paths_distances = []

        for cluster in self.trucks:
            start_delivery = next(delivery for delivery in cluster.deliveries if delivery.is_start)
            path, distance = cluster.tsp_path(start_delivery)
            paths_distances.append((path, distance))

        return paths_distances
    
    def solve_antoine(self):
        """Solve the TSP for each cluster and return the paths and distances."""
        paths_distances = []

        for cluster in self.trucks:
            start_delivery = next(delivery for delivery in cluster.deliveries if delivery.is_start)
            path, distance = cluster.antoine_algorithm(start_delivery)
            paths_distances.append((path, distance))

        return paths_distances