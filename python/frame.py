import numpy
import pygame

from entity import Entity
from state import State


class Frame(Entity):
    COOLDOWN = 1000
    def __init__(self, x: int, y: int, state: State):
        super().__init__(x, y, (27, 27))
        self.color_map = numpy.ndarray(self.resolution, dtype=numpy.int32)
        self.color_map.fill(0xfa78ff)
        self.height_map = numpy.ndarray(self.resolution, dtype=numpy.int32)
        self.height_map.fill(27)
        self.last = pygame.time.get_ticks()
    
    def get_color_map(self) -> numpy.ndarray:
        return self.color_map
    
    def get_height_map(self) -> numpy.ndarray:
        return self.height_map
    
    def terraforming(self, height_map: numpy.ndarray):
        now = pygame.time.get_ticks()
        if now - self.last >= self.COOLDOWN:
            self.last = now
            for x in range(max(0, self.pos_x - 60), min(499, self.pos_x + 60) + 1):
                for y in range(max(0, self.pos_y - 60), min(499, self.pos_y + 60) + 1):
                    if height_map[x, y] & 0xFF > 0x82:
                        height_map[x, y] = height_map[x, y] - 1
                    elif height_map[x, y] & 0xFF < 0x82:
                        height_map[x, y] = height_map[x, y] + 1
        
        return height_map

    def render(self, color_map: numpy.ndarray, height_map: numpy.ndarray):
        return super().render(color_map, height_map)
        
        
