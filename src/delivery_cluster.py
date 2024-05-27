from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
from delivery import Delivery

class DeliveryCluster:
    def __init__(self, cities):
        self.cities = cities

    def tsp_path(self, start_delivery):
        """Solve the TSP problem for the cluster starting from start_delivery using OR-Tools."""
        manager = pywrapcp.RoutingIndexManager(len(self.cities), 1, self.cities.index(start_delivery))
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_delivery = self.cities[manager.IndexToNode(from_index)]
            to_delivery = self.cities[manager.IndexToNode(to_index)]
            return int(self.calculate_distance(from_delivery, to_delivery) * 1000)  # Convert to integer

        transit_callback_index = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = (
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC)

        solution = routing.SolveWithParameters(search_parameters)

        if not solution:
            return None, None

        index = routing.Start(0)
        path = []
        while not routing.IsEnd(index):
            path.append(self.cities[manager.IndexToNode(index)])
            index = solution.Value(routing.NextVar(index))
        path.append(self.cities[manager.IndexToNode(index)])  # Return to start delivery

        return path, solution.ObjectiveValue() / 1000  # Convert back to float
    
    def antoine_algorithm(self, start_delivery):
        """Solve the TSP problem for the cluster starting from start_delivery using Antoine's algorithm."""
        """This algorithm creates a list of clusters, each containing a single delivery."""
        """It then iteratively merges the two closest endpoints until only one cluster remains."""
        """The result is the path of deliveries in the order they should be visited. So the order is important."""

        def reorder_path(path, start_delivery):
            """Reorder the path so that it starts from the start_delivery."""
            start_index = path.index(start_delivery)
            return path[start_index:] + path[:start_index] + [start_delivery]

        clusters = [[delivery] for delivery in self.cities]

        # Merge the two closest clusters until only one remains
        while len(clusters) > 1:
            closest_clusters = None
            case_closest_clusters = None
            min_distance = float('inf')

            for i in range(len(clusters)):
                for j in range(i + 1, len(clusters)):
                    case_1 = self.calculate_distance(clusters[i][0], clusters[j][0])
                    case_2 = self.calculate_distance(clusters[i][-1], clusters[j][0])
                    case_3 = self.calculate_distance(clusters[i][0], clusters[j][-1])
                    case_4 = self.calculate_distance(clusters[i][-1], clusters[j][-1])
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

        path_length = 0
        for i in range(len(clusters[0]) - 1):
            path_length += self.calculate_distance(clusters[0][i], clusters[0][i + 1])

        return reorder_path(clusters[0], start_delivery), path_length

    @staticmethod
    def calculate_distance(delivery1, delivery2):
        """Calculate Euclidean distance between two cities."""
        return np.linalg.norm(np.array(delivery1.coordinates) - np.array(delivery2.coordinates))