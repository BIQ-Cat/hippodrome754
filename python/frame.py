import numpy
from entity import Entity


class Frame(Entity):

    def __init__(self, x: int, y: int):
        super().__init__(x, y, (27, 27))
        self.color_map = numpy.zeros(self.resolution, dtype=numpy.int64)
        self.color_map.fill(0XAABBCC)
        self.height_map = numpy.ndarray(self.resolution, dtype=numpy.int64)
        self.height_map.fill(25)
    
    def get_color_map(self) -> numpy.ndarray:
        return self.color_map
    
    def get_height_map(self) -> numpy.ndarray:
        return self.height_map

    def render(self, color_map: numpy.ndarray, height_map: numpy.ndarray):
        return super().render(color_map, height_map)
        
        
