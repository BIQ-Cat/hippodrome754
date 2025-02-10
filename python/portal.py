import numpy
from entity import Entity
from state import State


class Portal(Entity):
    def __init__(self, x: int, y: int, state: State):
        super().__init__(x, y, (30, 20), state)
        self.color_map = numpy.ndarray(self.resolution, dtype=numpy.int32)
        self.height_map = numpy.ndarray(self.resolution, dtype=numpy.int32)
        self.__load_color_map()
        self.__load_height_map()
    
    def __load_color_map(self):
        self.color_map.fill(0xdadef1)
    
    def __load_height_map(self):
        self.height_map.fill(75)
    
    def get_height_map(self) -> numpy.ndarray:
        return self.height_map
    
    def get_color_map(self) -> numpy.ndarray:
        return self.color_map
    
    