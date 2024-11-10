from .a_star import AStar
from .bfs import BFS
from .dfs import DFS
from .ucs import UCS

ALGORITHMS_DICT = {
    "BFS": BFS,
    "DFS": DFS,
    "UCS": UCS,
    "A*": AStar
}