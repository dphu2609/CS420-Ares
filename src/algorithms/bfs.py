from collections import deque
from src.algorithms.base_algo import BaseAlgo
from src.map_data import MapData
from utils.calculate_goal_state import get_initial_state_and_goal_state
from utils.bfs_dfs_utils import measure_memory_and_time, generate_new_state, check_if_reach_goal_state


class BFS(BaseAlgo):
    def __init__(self):
        self.time = 0
        self.result = None
        self.memory = 0

    def run(self) -> bool:
        result, time, memory = self.run_bfs()
        self.time = time
        self.memory = memory
        self.result = result
        print("Result:", result)
        print("Nodes expanded:", self.nodes_expanded)
        print("Total weight pushed:", self.total_weight_pushed)
        print("Path:", self.path)
        print(f"Time taken: {time:.2f} ms")
        print(f"Peak memory usage: {memory:.4f} MB")
        return result
    
    def get_stats(self):
        return self.time / 1000, self.memory, self.nodes_expanded

    def set_map(self, map: MapData):
        self.map = map
        self.initial_state, self.goal_state = get_initial_state_and_goal_state(map)
        self.stones_weight = map.get_stones_weight()
        print("Initial state:", self.initial_state)
        print("Goal state:", self.goal_state)
        self.path = []
        self.map_matrix = map.get_map_matrix()
        self.nodes_expanded = 0
        self.total_weight_pushed = 0

    def get_map(self) -> MapData:
        return self.map

    def get_path(self):
        return self.path, self.map, self.total_weight_pushed

    @measure_memory_and_time
    def run_bfs(self):
        DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        queue = deque()
        visited = set()

        initial_state = (self.initial_state[0], tuple(self.initial_state[1]), [], 0)
        queue.append(initial_state)
        visited.add((initial_state[0], initial_state[1]))

        self.nodes_expanded = 1

        while queue:
            current_state = queue.popleft()

            if check_if_reach_goal_state(current_state, self.goal_state):
                self.path = current_state[2]
                self.total_weight_pushed = current_state[3]
                return True

            for direction in DIRECTIONS:
                new_state = generate_new_state(current_state, direction, self.map_matrix, self.stones_weight)
                if new_state:
                    new_key = (new_state[0], new_state[1])
                    if new_key not in visited:
                        self.nodes_expanded += 1
                        queue.append(new_state)
                        visited.add(new_key)

        return False