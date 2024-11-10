from .base_algo import BaseAlgo
from ..map_data import MapData
from .heuristic_utils import calculate_heuristic

import heapq, time, psutil

class Node:
    def __init__(self, current, parent=None):
        self.current = current
        self.parent = parent
        self.previous_move = None
        self.f = float('inf') # cost only because we are using UCS

class UCS(BaseAlgo):
    def __init__(self):
        self.map = None
        self.start_hash = None
        self.goal_hash = None

        self.game_state_dict = {} # map hash value to game state
        self.node_dict = {}

        self.time_consumed = 0
        self.memory_consumed = 0

    def set_map(self, map: MapData):
        self.map = map

    def is_goal(self, map: MapData) -> bool:
        return calculate_heuristic(map) == 0

    def run(self) -> bool:
        start_time = time.time()    
        self.memory_consumed = psutil.Process().memory_info().rss / 1024 / 1024

        self.game_state_dict = {}
        self.node_dict = {}

        open_list = []

        hash_start = self.map.hash_map()
        self.game_state_dict[hash_start] = self.map
        node_start = Node(hash_start)
        node_start.f = 0
        self.node_dict[hash_start] = node_start
        self.start_hash = hash_start
        heapq.heappush(open_list, (0, hash_start))

        while open_list:
            f, hash_current = heapq.heappop(open_list)
            current = self.game_state_dict[hash_current]
            node_current = self.node_dict[hash_current]

            if self.is_goal(self.game_state_dict[hash_current]):
                self.goal_hash = hash_current
                self.time_consumed = time.time() - start_time
                self.memory_consumed = psutil.Process().memory_info().rss / 1024 / 1024 - self.memory_consumed
                return True

            for move in current.get_possible_moves():
                new_map = current.copy()
                c = new_map.move(move).get_move_cost()
                hash_new = new_map.hash_map()

                if hash_new not in self.game_state_dict:
                    self.game_state_dict[hash_new] = new_map
                    node_new = Node(hash_new, node_current)
                    node_new.f = f + c
                    node_new.previous_move = move
                    if c > 1:
                        node_new.previous_move = move.upper()
                    self.node_dict[hash_new] = node_new
                    heapq.heappush(open_list, (node_new.f, hash_new))
                else:
                    node_new = self.node_dict[hash_new]
                    if node_new.f > f + c:
                        node_new.f = f + c
                        node_new.parent = node_current
                        node_new.previous_move = move
                        if c > 1:
                            node_new.previous_move = move.upper()
                        heapq.heappush(open_list, (node_new.f, hash_new))

        return False


    def get_map(self) -> MapData:
        pass

    def get_path(self):
        path = []
        maps = []

        current = self.goal_hash
        while current != self.start_hash:
            path.append(self.node_dict[current].previous_move)
            maps.append(self.game_state_dict[current].get_display_map())
            current = self.node_dict[current].parent.current

        pushed_weight = self.node_dict[self.goal_hash].f - len(path) + 1

        return path[::-1], maps[::1], pushed_weight
    
    def get_stats(self):
        return self.time_consumed, self.memory_consumed, len(self.node_dict)