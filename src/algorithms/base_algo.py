import abc
from ..map_data import MapData

class BaseAlgo(abc.ABC):
    @abc.abstractmethod
    def run(self) -> bool:
        pass

    @abc.abstractmethod
    def set_map(self, map: MapData):
        pass

    @abc.abstractmethod
    def get_map(self) -> MapData:
        pass

    @abc.abstractmethod
    def get_path(self) -> list:
        pass