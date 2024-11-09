from collections import deque
from scipy.optimize import linear_sum_assignment
import numpy as np
from src.algorithms.base_algo import BaseAlgo
from src.map_data import MapData

DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

def calculate_distances(map_matrix, start):
    distances_matrix = [[float('inf') for _ in range(len(map_matrix[0]))] for _ in range(len(map_matrix))]
    queue = deque([start])
    visited = [[False for _ in range(len(map_matrix[0]))] for _ in range(len(map_matrix))]

    start_x, start_y = start[0], start[1]
    start_weight = start[2]
    distances_matrix[start_x][start_y] = 0
    visited[start_x][start_y] = True

    while queue:
        current = queue.popleft()
        for dx, dy in DIRECTIONS:
            next_x, next_y = current[0] + dx, current[1] + dy
            if (0 <= next_x < len(map_matrix) and
                    0 <= next_y < len(map_matrix[0]) and
                    not visited[next_x][next_y] and
                    map_matrix[next_x][next_y] != MapData.BLOCKER
                    and map_matrix[next_x][next_y] <= 0):
                queue.append((next_x, next_y))
                visited[next_x][next_y] = True
                distances_matrix[next_x][next_y] = distances_matrix[current[0]][current[1]] + start_weight
    return distances_matrix

def construct_cost_matrix(map_matrix, stones_positions_weight, switches_positions):
    cost_matrix = [[float('inf')] * len(switches_positions) for _ in stones_positions_weight]

    for stone_index, stone in enumerate(stones_positions_weight):    
        distances_matrix = calculate_distances(map_matrix, stone)  # stone is (x, y, weight, index)
        for switch_index, switch in enumerate(switches_positions):
            switch_x, switch_y, _ = switch
            cost_matrix[stone_index][switch_index] = distances_matrix[switch_x][switch_y]

    return cost_matrix


from scipy.optimize import linear_sum_assignment
import numpy as np

def get_initial_state_and_goal_state(map_data: MapData):
    map_matrix = map_data.get_map_matrix()
    stones_weight = map_data.get_stones()
    current_position = map_data.get_current_position()
    
    stones_positions = []
    stones_positions_weight = []
    switches_positions = []
    stone_index = 0
    switch_index = 0

    for i in range(len(map_matrix)):
        for j in range(len(map_matrix[i])):
            if map_matrix[i][j] > 0:
                stones_positions.append((i, j))
                stones_positions_weight.append((i, j, stones_weight[stone_index], stone_index))
                stone_index += 1
            elif map_matrix[i][j] == map_data.SWITCH or map_matrix[i][j] == map_data.ARES_ON_SWITCH:
                switches_positions.append((i, j, switch_index))
                switch_index += 1

    cost_matrix = construct_cost_matrix(map_matrix, stones_positions_weight, switches_positions)

    # Ensure valid assignments
    cost_matrix = np.array(cost_matrix)
    if np.all(np.isinf(cost_matrix), axis=0).any() or np.all(np.isinf(cost_matrix), axis=1).any():
        raise ValueError("Cost matrix contains infeasible rows or columns with all infinite values.")

    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    stone_initial_state = stones_positions
    pair = []
    stone_goal_state = []
    
    for r, c in zip(row_ind, col_ind):
        pair.append((stones_positions_weight[r], switches_positions[c]))

    for _, switch in pair:
        stone_goal_state.append(switch[:2])

    initial_state = (current_position, stone_initial_state)
    goal_state = (current_position, stone_goal_state)

    return initial_state, goal_state

class BFS(BaseAlgo):
    def __init__(self):
        pass

    def run(self) -> bool:
        # Implementation placeholder
        pass

    def set_map(self, map: MapData):
        self.map = map
        initial_state, goal_state = get_initial_state_and_goal_state(map)
        print(initial_state)
        print(goal_state)


    def get_map(self) -> MapData:
        return self.map

    def get_path(self) -> list:
        # Implementation placeholder
        pass