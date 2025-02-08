import ctypes
import io
import os
import pathlib

import numpy
import pygame as pg

from map import Map
from state import State


class Camera(ctypes.Structure):
    _fields_ = [('x', ctypes.c_double), ('y', ctypes.c_double),
                ('angle', ctypes.c_double), ('height', ctypes.c_double),
                ('pitch', ctypes.c_double)]


class Screen(ctypes.Structure):
    _fields_ = [('width', ctypes.c_int), ('height', ctypes.c_int)]


class GoSlice(ctypes.Structure):
    _fields_ = [('data', ctypes.POINTER(ctypes.c_void_p)),
                ('len', ctypes.c_longlong), ("cap", ctypes.c_longlong)]


libname = pathlib.Path(__file__).parent.parent.resolve() / 'ray_casting'
if os.name == 'nt':
    dll = ctypes.CDLL(str(libname) + '.dll')

else:
    dll = ctypes.CDLL(str(libname) + '.so')

dll.RayCasting.argtypes = [
    Camera, Screen, ctypes.c_double, ctypes.c_int, ctypes.c_int,
    numpy.ctypeslib.ndpointer(numpy.int64),
    numpy.ctypeslib.ndpointer(numpy.int64), ctypes.c_int, ctypes.c_int,
    ctypes.c_double
]
dll.RayCasting.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))


class Render:

    def __init__(self,
                 screen: pg.Surface,
                 state: State,
                 map: Map,
                 resolution=tuple((500, 500))):
        self.screen = screen
        self.state = state
        self.height_map = map.get_height_map().flat.copy()
        self.color_map = map.get_height_map().flat.copy()
        self.resolution = resolution

    def set_color_map(self, color_map: numpy.ndarray):
        self.color_map = color_map.flat.copy()

    def set_height_map(self, height_map: numpy.ndarray):
        self.height_map = height_map.flat.copy()
    
    def set_maps(self, maps: tuple[numpy.ndarray, numpy.ndarray]):
        self.color_map = maps[0].flat.copy()
        self.height_map = maps[1].flat.copy()

    def set_resolution(self, resolution: tuple[int, int]):
        self.resolution = resolution

    def rayCasting(self):
        c_screen = dll.RayCasting(
            Camera(self.state.camera.get_x(), self.state.camera.get_y(),
                   self.state.camera.get_angle(),
                   self.state.camera.get_height(),
                   self.state.camera.get_pitch()),
            Screen(self.state.SCREEN_WIDTH, self.state.SCREEN_HEIGHT),
            self.state.RAY_CASTING_DELTA_ANGLE, self.state.SCALE_HEIGHT,
            self.state.RAY_CASTING_RAY_DISTANCE, self.color_map,
            self.height_map, self.resolution[0], self.resolution[1],
            self.state.FOV)

        screen = [[
            int(c_screen[i][j]) for j in range(self.state.SCREEN_HEIGHT)
        ] for i in range(self.state.SCREEN_WIDTH)]

        screen_array = numpy.array(screen, dtype=numpy.int64)

        return screen_array

    def draw(self):
        screen_array = self.rayCasting()
        pg.surfarray.blit_array(self.screen, screen_array)
