import abc
import numpy

from state import State


class Entity(abc.ABC):
    def __init__(self, x: int, y: int, resolution: tuple[int, int], state: State):
        self.pos_x = x
        self.pos_y = y
        self.resolution = resolution
        self.state = state

    @abc.abstractmethod
    def get_color_map(self) -> numpy.ndarray:
        pass

    @abc.abstractmethod
    def get_height_map(self) -> numpy.ndarray:
        pass

    def update_x(self, x: int):
        self.pos_x = x

    def update_y(self, y: int):
        self.pos_y = y

    def get_width(self):
        return self.pos_x + self.resolution[0]

    def get_height(self):
        return self.pos_y + self.resolution[1]
    
    def get_terraforming_size(self) -> int:
        return self.state.DISABLE_TERRAFORMING
    
    def terraforming(self, height_map: numpy.ndarray):
        if self.get_terraforming_size() == self.state.DISABLE_TERRAFORMING:
            return height_map

        terraforming_size = self.get_terraforming_size()
        
        max_x = min(self.state.MAP_RESOLUTION[0], self.get_width() + terraforming_size + 1)
        max_y = min(self.state.MAP_RESOLUTION[1], self.get_height() + terraforming_size + 1)

        for x in range(max(0, self.pos_x - terraforming_size), max_x):
            for y in range(max(0, self.pos_y - terraforming_size), max_y):
                if height_map[x, y] & self.state.GET_HEIGHT > self.state.ZERO_LAYER_HEIGHT:
                    height_map[x, y] = height_map[x, y] - 1
                elif height_map[x, y] & self.state.GET_HEIGHT < self.state.ZERO_LAYER_HEIGHT:
                    height_map[x, y] = height_map[x, y] + 1
        
        return height_map

    def render(self, color_map: numpy.ndarray, height_map: numpy.ndarray):
        res_color = color_map
        entitiy_color = self.get_color_map()

        res_height = height_map
        entity_height = self.get_height_map()

        for x in range(self.resolution[0]):
            for y in range(self.resolution[1]):
                map_pos = (x + self.pos_x, y + self.pos_y)
                res_color[map_pos] = entitiy_color[x, y]
                res_height[map_pos] = entity_height[x, y] + self.state.ZERO_LAYER_COLOR

        return (res_color, res_height)

        
