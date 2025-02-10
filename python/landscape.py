import ctypes
import io
import os
import pathlib

import numpy
import pygame as pg

from map import Map
from entity import Entity
from core import Core
from frame import Frame
from portal import Portal
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
    numpy.ctypeslib.ndpointer(numpy.int32),
    numpy.ctypeslib.ndpointer(numpy.int32), ctypes.c_int, ctypes.c_int,
    ctypes.c_double
]
dll.RayCasting.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))


class Landscape:
    def __init__(self,
                 screen: pg.Surface,
                 state: State,
                 map: Map,
                 resolution=tuple((500, 500)), *enitities: Entity):
        self.screen = screen
        self.state = state
        self.height_map = map.get_height_map().copy()
        self.color_map = map.get_height_map().copy()
        self.resolution = resolution
        self.entity_list = [Frame(127, 127, state)] + list(enitities)

    def set_color_map(self, color_map: numpy.ndarray):
        self.color_map = color_map.copy()

    def set_height_map(self, height_map: numpy.ndarray):
        self.height_map = height_map.copy()

    def set_resolution(self, resolution: tuple[int, int]):
        self.resolution = resolution

    def rayCasting(self, color_map: numpy.ndarray, height_map: numpy.ndarray):
        c_screen = dll.RayCasting(
            Camera(self.state.camera.get_x(), self.state.camera.get_y(),
                   self.state.camera.get_angle(),
                   self.state.camera.get_height(),
                   self.state.camera.get_pitch()),
            Screen(self.state.SCREEN_WIDTH, self.state.SCREEN_HEIGHT),
            self.state.RAY_CASTING_DELTA_ANGLE, self.state.SCALE_HEIGHT,
            self.state.RAY_CASTING_RAY_DISTANCE, color_map,
            height_map, self.resolution[0], self.resolution[1],
            self.state.FOV)

        screen = [[
            int(c_screen[i][j]) for j in range(self.state.SCREEN_HEIGHT)
        ] for i in range(self.state.SCREEN_WIDTH)]

        screen_array = numpy.array(screen, dtype=numpy.int32)

        return screen_array
    
    def terraforming(self):
        for entity in self.entity_list:
            self.height_map = entity.terraforming(self.height_map)
    
    def check_win(self, portal: Portal):
        if not self.state.new_core_built:
            return False
        
        self.state.new_core_built = False
        last_core = self.entity_list[-1]
        
        return portal.pos_x - 5 <= last_core.pos_x <= portal.get_width() + 5 and \
               portal.pos_y - 5 <= last_core.pos_y <= portal.get_height() + 5
    
    def update(self):
        key = pg.key.get_pressed()
        if key[pg.K_SPACE] and not self.state.has_prebulid_core:
            self.entity_list.append(Core(130, 130, self.state))
            self.state.has_prebulid_core = True


    def render(self):
        color_map = self.color_map.copy()
        height_map = self.height_map.copy()
        
        for entity in self.entity_list:
            color_map, height_map = entity.render(color_map, height_map)
        
        screen_array = self.rayCasting(color_map.flat.copy(), height_map.flat.copy())
        pg.surfarray.blit_array(self.screen, screen_array)
