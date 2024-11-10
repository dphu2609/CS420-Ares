import numpy as np
from ..map_data import MapData
from scipy.optimize import linear_sum_assignment

def hungarian_algorithm(cost_matrix: np.ndarray) -> float:
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    
    return cost_matrix[row_ind, col_ind].sum()

def convert_map_to_cost_matrix(map_data: MapData) -> np.ndarray:
    weighed_stones, position_stones = map_data.get_stones()
    goals = map_data.get_switches()

    n = len(goals)

    cost_matrix = np.zeros((n, n))
    for i in range(1, len(position_stones)):
        for j in range(n):
            cost_matrix[i-1][j] = abs(position_stones[i][0] - goals[j][0]) + abs(position_stones[i][1] - goals[j][1])
            cost_matrix[i-1][j] = cost_matrix[i-1][j] * weighed_stones[i]

    return cost_matrix

def static_vars(**kwargs):
    def decorate(func):
        for k in kwargs:
            setattr(func, k, kwargs[k])
        return func
    return decorate


@static_vars(heuristic_memory={})
def calculate_heuristic(map_data: MapData) -> float:
    weighed_stones, position_stones = map_data.get_stones()
    goals = map_data.get_switches()

    # Convert position_stones and goals to tuples and hash them
    position_stones_tuple = tuple(map(tuple, position_stones[1:]))
    goals_tuple = tuple(map(tuple, goals))
    hash_val = hash((position_stones_tuple, goals_tuple))
    
    # Check if the heuristic has already been calculated
    if hash_val in calculate_heuristic.heuristic_memory:
        return calculate_heuristic.heuristic_memory[hash_val]
    else:
        heuristic = hungarian_algorithm(convert_map_to_cost_matrix(map_data))
        calculate_heuristic.heuristic_memory[hash_val] = heuristic
        return heuristic