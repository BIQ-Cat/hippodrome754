import math
import pathlib

import pygame as pg

from .camera import Camera


class State:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 450

    FPS = 60

    FOV = math.pi / 6
    RAY_CASTING_DELTA_ANGLE = FOV / SCREEN_WIDTH
    RAY_CASTING_RAY_DISTANCE = 2000
    SCALE_HEIGHT = 980

    ZERO_LAYER_COLOR = 0x828282
    GET_HEIGHT = 0xFF
    ZERO_LAYER_HEIGHT = ZERO_LAYER_COLOR & GET_HEIGHT
    DISABLE_TERRAFORMING = 0

    MAP_RESOLUTION = (500, 500)
    MAP_DIR = pathlib.Path(__file__).parent.parent.resolve() / 'img'
    
    SOUND_DIR = pathlib.Path(__file__).parent.parent.resolve() / 'sounds'

    def __init__(self, camera: Camera):
        self.camera = camera

        self.has_prebulid_core = False
        self.new_core_built = False
        
        self.lost = False
