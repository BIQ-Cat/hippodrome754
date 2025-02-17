import numpy
from PIL import Image

from .entity import Entity
from .state import State


class Portal(Entity):
    WIN_DIFF = 10
    def __init__(self, x: int, y: int, state: State):
        super().__init__(x, y, (25, 25), state)
        self.color_map = self.__load_map(True)
        self.height_map = self.__load_map(False)

    def __load_map(self, is_color_map):
        array = numpy.ndarray(self.resolution, dtype=numpy.int32)

        if is_color_map:
            img = Image.open(str(self.state.MAP_DIR / "portal_color_map.jpg"))

        else:
            img = Image.open(str(self.state.MAP_DIR / "portal_height_map.jpg"))
        
        pixels = img.load()
        for y in range(self.resolution[1]):
            for x in range(self.resolution[0]):
                r, g, b = pixels[x, y]  # type: ignore
                
                array[x, y] = r * 65536 + g * 256 + b

        return array
    
    def get_height_map(self) -> numpy.ndarray:
        return self.height_map
    
    def get_color_map(self) -> numpy.ndarray:
        return self.color_map
    
    