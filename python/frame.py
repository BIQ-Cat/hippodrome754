import numpy
import pygame

from entity import Entity
from state import State


class Frame(Entity):
    COOLDOWN = 1000
    RESOLUTION = (27, 27)
    def __init__(self, x: int, y: int, state: State):
        super().__init__(x, y, self.RESOLUTION, state)
        self.color_map = numpy.ndarray(self.resolution, dtype=numpy.int32)
        self.height_map = numpy.ndarray(self.resolution, dtype=numpy.int32)
        self.last = pygame.time.get_ticks()

        self.__load_color_map()
        self.__load_height_map()
    
    def __load_color_map(self):
        self.color_map.fill(0xfadb78)
    
    def __load_height_map(self):
        self.height_map.fill(27)
    
    
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
        
        
