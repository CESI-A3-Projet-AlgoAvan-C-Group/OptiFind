from sklearn.cluster import KMeans
import numpy as np
from city import City
from city_cluster import CityCluster

class CityClusterer:
    def __init__(self, cities, n_clusters):
        self.cities = cities
        self.n_clusters = n_clusters
        self.clusters = []

    def cluster_cities(self):
        coordinates = np.array([city.coordinates for city in self.cities])
        kmeans = KMeans(n_clusters=self.n_clusters, n_init=10)
        labels = kmeans.fit_predict(coordinates)
        
        self.clusters = [CityCluster([]) for _ in range(self.n_clusters)]
        start_index = next(i for i, city in enumerate(self.cities) if city.is_start)
        
        # Ensure the starting city is in every cluster
        for cluster in self.clusters:
            cluster.cities.append(self.cities[start_index])
    
        for city, label in zip(self.cities, labels):
            if not city.is_start:  # The starting city is already added to all clusters
                self.clusters[label].cities.append(city)
        
        return self.clusters