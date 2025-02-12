import numpy
import pygame
from PIL import Image

from entity import Entity
from state import State


class Frame(Entity):
    COOLDOWN = 1000
    RESOLUTION = (25, 25)
    def __init__(self, x: int, y: int, state: State):
        super().__init__(x, y, self.RESOLUTION, state)
        self.color_map = self.__load_map(True)
        self.height_map = self.__load_map(False)
        
        self.last = pygame.time.get_ticks()

    def __load_map(self, is_color_map):
        array = numpy.ndarray(self.resolution, dtype=numpy.int32)

        if is_color_map:
            img = Image.open(str(self.state.MAP_DIR / "frame_color_map.jpg"))

        else:
            img = Image.open(str(self.state.MAP_DIR / "frame_height_map.jpg"))
        
        pixels = img.load()
        for y in range(self.resolution[1]):
            for x in range(self.resolution[0]):
                r, g, b = pixels[x, y]  # type: ignore
                
                array[x, y] = r * 65536 + g * 256 + b

        return array

    def __load_height_map(self):
        pass
    
    def get_color_map(self) -> numpy.ndarray:
        return self.color_map
    
    def get_height_map(self) -> numpy.ndarray:
        return self.height_map
    
    def get_terraforming_size(self) -> int:
        return 60
    
    def terraforming(self, height_map: numpy.ndarray):
        now = pygame.time.get_ticks()
        if now - self.last >= self.COOLDOWN:
            self.last = now
            return super().terraforming(height_map)

        return height_map

    def render(self, color_map: numpy.ndarray, height_map: numpy.ndarray):
        return super().render(color_map, height_map)
        
        
