from collections import deque
from scipy.optimize import linear_sum_assignment
import numpy as np
from base_algo import BaseAlgo
from ..map_data import MapData


class BFS(BaseAlgo):
    DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    def __init__(self):
        self.map = None
        self.map_matrix = None
        self.distances_matrix = None
        self.cost_matrix = None
        self.stones_positions_weight = []
        self.switches_positions = []

    def set_map(self, map: MapData):
        self.map = map
        self.map_matrix = map.get_map_matrix()
        current_position = map.get_current_position()
        stones_weight = map.get_stones()

        self.stone_positions = []
        self.stones_positions_weight = []
        self.switches_positions = []

        stone_index = 0
        switch_index = 0

        for i in range(len(self.map_matrix)):
            for j in range(len(self.map_matrix[i])):
                if self.map_matrix[i][j] > 0:
                    self.stone_positions.append((i, j))
                    self.stones_positions_weight.append((i, j, stones_weight[stone_index], stone_index))
                    stone_index += 1
                elif self.map_matrix[i][j] == map.SWITCH:
                    self.switches_positions.append((i, j, switch_index))
                    switch_index += 1

        self.distances_matrix = [[float('inf') for _ in range(len(self.map_matrix[0]))] for _ in range(len(self.map_matrix))]
        self.cost_matrix = [[0 for _ in range(len(self.stones_positions_weight))] for _ in range(len(self.switches_positions))]
        self.initial_state = (current_position, self.stone_positions, self.switches_positions)

    def bfs(self, stone):
        queue = deque([stone])
        visited = [[False for _ in range(len(self.map_matrix[0]))] for _ in range(len(self.map_matrix))]
        self.distances_matrix = [[float('inf') for _ in range(len(self.map_matrix[0]))] for _ in range(len(self.map_matrix))]

        start_x, start_y = stone[:2]
        visited[start_x][start_y] = True
        self.distances_matrix[start_x][start_y] = 0

        while queue:
            current = queue.popleft()
            for dx, dy in self.DIRECTIONS:
                next_x, next_y = current[0] + dx, current[1] + dy
                if (0 <= next_x < len(self.map_matrix) and
                        0 <= next_y < len(self.map_matrix[0]) and
                        not visited[next_x][next_y] and
                        self.map_matrix[next_x][next_y] != self.map.BLOCKER):
                    queue.append((next_x, next_y))
                    visited[next_x][next_y] = True
                    self.distances_matrix[next_x][next_y] = self.distances_matrix[current[0]][current[1]] + 1

    def add_to_cost_matrix(self, stone):
        _, _, _, index = stone
        for switch in self.switches_positions:
            self.cost_matrix[index][switch[2]] = self.distances_matrix[switch[0]][switch[1]]

    def construct_cost_matrix(self):
        for stone in self.stones_positions_weight:
            self.bfs(stone)
            self.add_to_cost_matrix(stone)

    def get_assignment(self):
        row_ind, col_ind = linear_sum_assignment(np.array(self.cost_matrix))
        return row_ind, col_ind
    
    def get_goal_state(self):
        assignment = self.get_assignment()
        goal_stones_positions = []
        for assign in assignment:
            goal_stones_positions.append(self.switches_positions[assign])

    def run(self) -> bool:
        # Implementation placeholder
        pass

    def check_goal_state(self) -> bool:
        # Implementation placeholder
        pass

    def get_map(self) -> MapData:
        return self.map

    def get_path(self) -> list:
        # Implementation placeholder
        pass
