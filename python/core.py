import numpy
import pygame
from entity import Entity
from camera import Camera
from state import State


class Core(Entity):
    COOLDOWN = 2000
    def __init__(self, x: int, y: int, state: State):
        super().__init__(x, y, (16, 16), state)
        self.height_map = numpy.ndarray(self.resolution, dtype=numpy.int32)
        self.color_maps = {
            "built": numpy.ndarray(self.resolution, dtype=numpy.int32),
            "can": numpy.ndarray(self.resolution, dtype=numpy.int32),
            "cannot": numpy.ndarray(self.resolution, dtype=numpy.int32)
        }
        
        self.camera = state.camera
        
        self.can_be_built = False
        self.prebuild_state = True
        
        self.last = pygame.time.get_ticks()

        self.__load_color_maps()
        self.__load_height_map()
    
    def __load_color_maps(self):
        self.color_maps["built"].fill(0x0000ff)
        self.color_maps["can"].fill(0x00ff00)
        self.color_maps["cannot"].fill(0xff0000)
    
    def __load_height_map(self):
        self.height_map.fill(10)
        self.height_map[4:12, 4:12].fill(27)

    
    def get_color_map(self) -> numpy.ndarray:        
        if not self.prebuild_state:
            return self.color_maps["built"]
        elif self.can_be_built:
            return self.color_maps["can"]
        else:
            return self.color_maps["cannot"]
        

    def get_terraforming_size(self):
        return 30

    def terraforming(self, height_map: numpy.ndarray):
        now = pygame.time.get_ticks()
        if now - self.last >= self.COOLDOWN:
            self.last = now
            if not self.prebuild_state:
                return super().terraforming(height_map)
        
        return height_map

    def get_height_map(self) -> numpy.ndarray:
        return self.height_map
    
    def pre_render(self, height_map: numpy.ndarray):
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
                    if height_map[x, y] & self.state.GET_HEIGHT != self.state.ZERO_LAYER_HEIGHT:
                        self.can_be_built = False
                        break
            
            if key[pygame.K_RETURN] and self.can_be_built:
                self.prebuild_state = False
                self.state.has_prebulid_core = False
                self.state.new_core_built = True

    
    def render(self, color_map: numpy.ndarray, height_map: numpy.ndarray):
        self.pre_render(height_map)

        res_color = color_map
        entitiy_color = self.get_color_map()

        res_height = height_map

        for x in range(self.resolution[0]):
            for y in range(self.resolution[1]):
                map_pos = (x + self.pos_x, y + self.pos_y)
                res_color[map_pos] = entitiy_color[x, y]
                res_height[map_pos] = self.height_map[x, y] + height_map[map_pos]

        return (res_color, res_height)