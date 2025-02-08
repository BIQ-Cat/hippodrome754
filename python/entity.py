import abc
import numpy

from map import Map


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

    def render(self, color_map: numpy.ndarray, height_map: numpy.ndarray):
        res_color = color_map
        entitiy_color = self.get_color_map()

        res_height = height_map
        entity_height = self.get_height_map()

        for x in range(self.resolution[0]):
            for y in range(self.resolution[1]):
                map_pos = (x + self.pos_x, y + self.pos_y)
                res_color[map_pos] = entitiy_color[x, y]
                res_height[map_pos] = entity_height[x, y] + 127

        return (res_color, res_height)


class EntityList(list[Entity]):
    def __init__(self, map: Map, *enitites: Entity):
        super().__init__(enitites)
        self.color_map = map.get_height_map()
        self.height_map = map.get_height_map()

    def set_color_map(self, color_map: numpy.ndarray):
        self.color_map = color_map

    def set_height_map(self, height_map: numpy.ndarray):
        self.height_map = height_map

    def generate_map(self):
        color_map = self.color_map
        height_map = self.height_map
        for entity in self:
            color_map, height_map = entity.render(color_map, height_map)

        return (color_map, height_map)
