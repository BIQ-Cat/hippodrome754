import math
import numpy
import pygame
from entity import Entity
from camera import Camera


class Core(Entity):
    COOLDOWN = 3000
    def __init__(self, x: int, y: int, camera: Camera):
        super().__init__(x, y, (16, 15))
        self.height_map = numpy.ndarray(self.resolution, dtype=numpy.int32)
        self.height_map.fill(10)
        self.height_map[4:10, 4:10].fill(27)
        
        self.camera = camera
        
        self.can_be_built = False
        self.prebuild_state = True
        
        self.last = pygame.time.get_ticks()
    
    def get_color_map(self) -> numpy.ndarray:
        res = numpy.ndarray(self.resolution, dtype=numpy.int32)
        
        if not self.prebuild_state:
            res.fill(0xff)
        elif self.can_be_built:
            res.fill(0x00ff00)
        else:
            res.fill(0xff0000)
        
        return res

    def terraforming(self, height_map: numpy.ndarray):
        now = pygame.time.get_ticks()
        if now - self.last >= self.COOLDOWN:
            self.last = now
            if not self.prebuild_state:
                for x in range(max(0, self.pos_x - 30), min(499, self.pos_x + 30) + 1):
                    for y in range(max(0, self.pos_y - 30), min(499, self.pos_y + 30) + 1):
                        if height_map[x, y] & 0xFF > 0x82:
                            height_map[x, y] = height_map[x, y] - 1
                        elif height_map[x, y] & 0xFF < 0x82:
                            height_map[x, y] = height_map[x, y] + 1
        
        return height_map

    def get_height_map(self) -> numpy.ndarray:
        return self.height_map
    
    def pre_render(self, color_map: numpy.ndarray, height_map: numpy.ndarray):
        if self.prebuild_state:
            key = pygame.key.get_pressed()
            
            if key[pygame.K_UP]:
                self.pos_x += self.camera.vel
                self.pos_y += self.camera.vel

            if key[pygame.K_DOWN]:
                self.pos_x -= self.camera.vel
                self.pos_y -= self.camera.vel

            if key[pygame.K_LEFT]:
                self.pos_x += self.camera.vel
                self.pos_y -= self.camera.vel

            if key[pygame.K_RIGHT]:
                self.pos_x -= self.camera.vel
                self.pos_y += self.camera.vel
                
            
            self.can_be_built = True
            
            for x in range(self.pos_x, self.pos_x + self.resolution[0]):
                if not self.can_be_built:
                    break
                
                for y in range(self.pos_y, self.pos_y + self.resolution[1]):
                    if height_map[x, y] & 0xFF != 0x82:
                        self.can_be_built = False
                        break
            
            if key[pygame.K_RETURN] and self.can_be_built:
                self.prebuild_state = False
            
        return super().pre_render(color_map, height_map)
    
    def render(self, color_map: numpy.ndarray, height_map: numpy.ndarray):
        res_color = color_map
        entitiy_color = self.get_color_map()

        res_height = height_map

        for x in range(self.resolution[0]):
            for y in range(self.resolution[1]):
                map_pos = (x + self.pos_x, y + self.pos_y)
                res_color[map_pos] = entitiy_color[x, y]
                res_height[map_pos] = self.height_map[x, y] + height_map[map_pos]

        return (res_color, res_height)