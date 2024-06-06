import numpy as np
import pandas as pd
import pulp
import itertools
import math

# Define the Haversine distance function
def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 6371.0  # Radius of Earth in kilometers
    distance = c * r * 1000  # Convert to meters
    return distance

# Parameters
customer_count = 10  # including depot
vehicle_count = 4
vehicle_capacity = 50

# Fix random seed for reproducibility
np.random.seed(777)

# Set depot coordinates
depot_latitude = 40.748817
depot_longitude = -73.985428

# Generate random customer locations and demands
df = pd.DataFrame({
    "latitude": np.random.normal(depot_latitude, 0.007, customer_count),
    "longitude": np.random.normal(depot_longitude, 0.007, customer_count),
    "demand": np.random.randint(10, 20, customer_count)
})

# Set the depot as the first row and make its demand zero
df.iloc[0] = [depot_latitude, depot_longitude, 0]

# Calculate distance matrix using Haversine function
def _distance_calculator(_df):
    _distance_result = np.zeros((len(_df), len(_df)))
    for i in range(len(_df)):
        for j in range(len(_df)):
            if i != j:
                _distance_result[i][j] = haversine(_df['latitude'][i], _df['longitude'][i],
                                                   _df['latitude'][j], _df['longitude'][j])
    return _distance_result

distance = _distance_calculator(df)

# Problem definition
problem = pulp.LpProblem("CVRP", pulp.LpMinimize)

# Decision variables
x = [[[pulp.LpVariable(f"x_{i}_{j}_{k}", cat="Binary") if i != j else None for k in range(vehicle_count)]
      for j in range(customer_count)] for i in range(customer_count)]

# Objective function
problem += pulp.lpSum(distance[i][j] * x[i][j][k] if i != j else 0
                      for k in range(vehicle_count)
                      for j in range(customer_count)
                      for i in range(customer_count))

# Constraints
# Each customer must be visited exactly once
for j in range(1, customer_count):
    problem += pulp.lpSum(x[i][j][k] if i != j else 0 for i in range(customer_count) for k in range(vehicle_count)) == 1

# Ensure that the vehicle enters and leaves each vertex exactly once
for k in range(vehicle_count):
    for j in range(customer_count):
        problem += (pulp.lpSum(x[i][j][k] if i != j else 0 for i in range(customer_count)) ==
                    pulp.lpSum(x[j][i][k] if j != i else 0 for i in range(customer_count)))

# Vehicle capacity constraints
for k in range(vehicle_count):
    problem += pulp.lpSum(df['demand'][j] * x[i][j][k] if i != j else 0
                          for i in range(customer_count) for j in range(customer_count)) <= vehicle_capacity

# Each tour must start and end at the depot
for k in range(vehicle_count):
    problem += pulp.lpSum(x[0][j][k] for j in range(1, customer_count)) == 1
    problem += pulp.lpSum(x[i][0][k] for i in range(1, customer_count)) == 1

# Subtour elimination constraints
subtours = []
for i in range(2, customer_count):
    subtours += itertools.combinations(range(1, customer_count), i)

for s in subtours:
    for k in range(vehicle_count):
        problem += pulp.lpSum(x[i][j][k] if i != j else 0 for i, j in itertools.permutations(s, 2)) <= len(s) - 1

# Solve the problem
problem.solve()

# Print results
if pulp.LpStatus[problem.status] == 'Optimal':
    print("Optimal solution found!")
    print("Vehicle Requirements:", vehicle_count)
    print("Total Distance:", pulp.value(problem.objective))
else:
    print("No optimal solution found.")

# Print the routes
for k in range(vehicle_count):
    route = []
    for i in range(customer_count):
        for j in range(customer_count):
            if i != j and pulp.value(x[i][j][k]) == 1:
                route.append((i, j))
    if route:
        print(f"Route for vehicle {k + 1}: {route}")

# Visualization with matplotlib
import matplotlib.pyplot as plt

plt.figure(figsize=(8, 8))
for i in range(customer_count):
    if i == 0:
        plt.scatter(df.latitude[i], df.longitude[i], c='green', s=200)
        plt.text(df.latitude[i], df.longitude[i], "depot", fontsize=12)
    else:
        plt.scatter(df.latitude[i], df.longitude[i], c='orange', s=200)
        plt.text(df.latitude[i], df.longitude[i], str(df.demand[i]), fontsize=12)

for k in range(vehicle_count):
    for i in range(customer_count):
        for j in range(customer_count):
            if i != j and pulp.value(x[i][j][k]) == 1:
                plt.plot([df.latitude[i], df.latitude[j]], [df.longitude[i], df.longitude[j]], c="black")

plt.show()