from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
from city import City

class CityCluster:
    def __init__(self, cities):
        self.cities = cities

    def tsp_path(self, start_city):
        """Solve the TSP problem for the cluster starting from start_city using OR-Tools."""
        manager = pywrapcp.RoutingIndexManager(len(self.cities), 1, self.cities.index(start_city))
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            from_city = self.cities[manager.IndexToNode(from_index)]
            to_city = self.cities[manager.IndexToNode(to_index)]
            return int(self.calculate_distance(from_city, to_city) * 1000)  # Convert to integer

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
        path.append(self.cities[manager.IndexToNode(index)])  # Return to start city

        return path, solution.ObjectiveValue() / 1000  # Convert back to float

    @staticmethod
    def calculate_distance(city1, city2):
        """Calculate Euclidean distance between two cities."""
        return np.linalg.norm(np.array(city1.coordinates) - np.array(city2.coordinates))