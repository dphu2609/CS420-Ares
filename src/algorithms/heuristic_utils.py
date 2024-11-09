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