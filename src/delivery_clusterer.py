from sklearn.cluster import KMeans
import numpy as np
from delivery import Delivery
from delivery_cluster import DeliveryCluster

class DeliveryClusterer:
    def __init__(self, cities, n_clusters):
        self.cities = cities
        self.n_clusters = n_clusters
        self.clusters = []

    def cluster_cities(self):
        coordinates = np.array([delivery.coordinates for delivery in self.cities])
        kmeans = KMeans(n_clusters=self.n_clusters, n_init=10)
        labels = kmeans.fit_predict(coordinates)
        
        self.clusters = [DeliveryCluster([]) for _ in range(self.n_clusters)]
        start_index = next(i for i, delivery in enumerate(self.cities) if delivery.is_start)
        
        # Ensure the starting delivery is in every cluster
        for cluster in self.clusters:
            cluster.cities.append(self.cities[start_index])
    
        for delivery, label in zip(self.cities, labels):
            if not delivery.is_start:  # The starting delivery is already added to all clusters
                self.clusters[label].cities.append(delivery)

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

        for cluster in self.clusters:
            start_delivery = next(delivery for delivery in cluster.cities if delivery.is_start)
            path, distance = cluster.tsp_path(start_delivery)
            paths_distances.append((path, distance))

        return paths_distances
    
    def solve_antoine(self):
        """Solve the TSP for each cluster and return the paths and distances."""
        paths_distances = []

        for cluster in self.clusters:
            start_delivery = next(delivery for delivery in cluster.cities if delivery.is_start)
            path, distance = cluster.antoine_algorithm(start_delivery)
            paths_distances.append((path, distance))

        return paths_distances