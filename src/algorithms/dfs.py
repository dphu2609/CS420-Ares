from base_algo import BaseAlgo
from ..map_data import MapData

class DFS(BaseAlgo):
    def __init__(self):
        self.map = None

    def set_map(self, map: MapData):
        self.map = map

    def run(self) -> bool:
        pass

    def get_map(self) -> MapData:
        pass

    def get_path(self) -> list:
        pass