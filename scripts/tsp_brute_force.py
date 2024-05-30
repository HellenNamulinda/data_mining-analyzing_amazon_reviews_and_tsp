from itertools import permutations
import math

# Distance matrix
distance_matrix = [
    [0, 12, 10, 24, 13, 21, 12],  # Distances from city 1
    [12, 0, 8, 12, 11, 17, 17],   # Distances from city 2
    [10, 8, 0, 11, 3, 9, 9],      # Distances from city 3
    [24, 12, 11, 0, 11, 10, 18],  # Distances from city 4
    [13, 11, 3, 11, 0, 6, 7],     # Distances from city 5
    [21, 17, 9, 10, 6, 0, 9],     # Distances from city 6
    [12, 17, 9, 18, 7, 9, 0]      # Distances from city 7
]

num_cities = len(distance_matrix)
cities = list(range(num_cities))

print(f'Number of Cities: {num_cities}')

# Calculate the possible number of paths
possible_paths = math.factorial(num_cities - 1)
print(f'Possible number of paths: {possible_paths}')

# Function to calculate the total distance of a given path
def calculate_distance(path):
    total_distance = 0
    for i in range(len(path) - 1):
        total_distance += distance_matrix[path[i]][path[i + 1]]
    total_distance += distance_matrix[path[-1]][path[0]]  # return to start
    return total_distance

# Brute-force approach to find the optimal path
def find_optimal_path():
    min_distance = float('inf')
    best_path = None
    for perm in permutations(cities[1:]):  # exclude starting city
        current_path = [0] + list(perm)
        current_distance = calculate_distance(current_path)
        if current_distance < min_distance:
            min_distance = current_distance
            best_path = current_path
    return best_path, min_distance

optimal_path, optimal_distance = find_optimal_path()

# Convert city indices to 1-based indexing for output and add the starting city at the end
optimal_path_1_based = [city + 1 for city in optimal_path] + [optimal_path[0] + 1]

print(f"Optimal Path: {optimal_path_1_based}")
print(f"Optimal Distance: {optimal_distance}")
