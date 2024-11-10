from .base_algo import BaseAlgo
from ..map_data import MapData
from .heuristic_utils import calculate_heuristic

import heapq, sys, time, psutil

class Node:
    def __init__(self, current, parent=None):
        self.current = current
        self.parent = parent
        self.previous_move = None
        self.f = float('inf')
        self.g = float('inf')
        self.h = float('inf')

class AStar(BaseAlgo):
    def __init__(self):
        self.map = None
        self.start_hash = None
        self.goal_hash = None

        self.game_state_dict = {} # map hash value to game state
        self.node_dict = {} # map hash value to node

        self.time_consumed = 0
        self.memory_consumed = 0

    # Should copy a new map
    def set_map(self, map: MapData):
        self.map = map

    def is_goal(self, map: MapData) -> bool:
        return calculate_heuristic(map) == 0

    def run(self) -> bool:
        start_time = time.time()
        self.memory_consumed = psutil.Process().memory_info().rss / 1024 / 1024 # in MB
        self.game_state_dict = {} # map hash value to game state
        self.node_dict = {} # map hash value to node
        open_list = []
        closed_list = {} # map hash value to f 
        
        hash_start = self.map.hash_map()
        self.game_state_dict[hash_start] = self.map
        node_start = Node(hash_start)
        node_start.f = 0
        node_start.g = 0
        node_start.h = 0
        self.node_dict[hash_start] = node_start
        self.start_hash = hash_start
        heapq.heappush(open_list, (0, hash_start))

        DEBUG = 0

        while open_list:
            f, hash_current = heapq.heappop(open_list)
            current = self.game_state_dict[hash_current]
            node_current = self.node_dict[hash_current]

            if self.is_goal(self.game_state_dict[hash_current]):
                self.goal_hash = hash_current
                self.time_consumed = time.time() - start_time
                self.memory_consumed = psutil.Process().memory_info().rss / 1024 / 1024 - self.memory_consumed
                return True

            # print current map
            # print("#########################")
            # print(f"Current map: {hash_current}")
            # for row in current.get_display_map():
            #     print(''.join(row))
            
            # DEBUG += 1
            # if DEBUG == 50:
            #     sys.exit(1)

            closed_list[hash_current] = f

            for move in current.get_possible_moves():
                new_map = current.copy()
                c = new_map.move(move).get_move_cost()
                hash_new = new_map.hash_map()
                if hash_new not in self.game_state_dict:
                    self.game_state_dict[hash_new] = new_map
                    node_new = Node(hash_new, node_current)
                    self.node_dict[hash_new] = node_new
                else:
                    node_new = self.node_dict[hash_new]
                
                if hash_new in closed_list:
                    continue

                if node_new.g > node_current.g + c:
                    node_new.g = node_current.g + c
                    node_new.h = calculate_heuristic(new_map)
                    node_new.f = node_new.g + node_new.h
                    node_new.previous_move = move
                    if c > 1:
                        node_new.previous_move = move.upper()
                    heapq.heappush(open_list, (node_new.f, hash_new))


    def get_map(self) -> MapData:
        pass

    # return list of path and list of maps
    def get_path(self):
        # Get the path from the start node to the goal node
        path = []
        maps = []
        current = self.goal_hash

        while current != self.start_hash:
            path.append(self.node_dict[current].previous_move)
            maps.append(self.game_state_dict[current].get_display_map())
            current = self.node_dict[current].parent.current

        return path[::-1], maps[::-1], self.node_dict[self.goal_hash].g
    
    def get_stats(self):
        return self.time_consumed, self.memory_consumed, len(self.node_dict)