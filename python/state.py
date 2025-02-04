import math
import pathlib

import pygame as pg

from camera import Camera


class State:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 450

    FPS = 60

    FOV = math.pi / 6
    RAY_CASTING_DELTA_ANGLE = FOV / SCREEN_WIDTH
    RAY_CASTING_RAY_DISTANCE = 2000
    SCALE_HEIGHT = 980

    MAP_DIR = pathlib.Path(__file__).parent.parent.resolve() / 'img'

    def __init__(self, camera: Camera):
        self.camera = camera

        self.color_map_path = self.MAP_DIR / 'color_map.jpg'
        self.height_map_path = self.MAP_DIR / 'height_map.jpg'
        self.load_maps()

    def load_maps(self):
        self.color_map_img = pg.image.load(self.color_map_path)
        self.color_map = pg.surfarray.array2d(self.color_map_img)

        self.height_map_img = pg.image.load(self.height_map_path)
        self.height_map = pg.surfarray.array2d(self.height_map_img)
