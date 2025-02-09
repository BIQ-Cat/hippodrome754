import abc
import numpy


class Entity(abc.ABC):

    def __init__(self, x: int, y: int, resolution: tuple[int, int]):
        self.pos_x = x
        self.pos_y = y
        self.resolution = resolution

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
    
    def pre_render(self, color_map: numpy.ndarray, height_map: numpy.ndarray):
        return (color_map, height_map)
    
    def terraforming(self, height_map: numpy.ndarray):
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
                res_height[map_pos] = entity_height[x, y] + 8553090

        return (res_color, res_height)

        
