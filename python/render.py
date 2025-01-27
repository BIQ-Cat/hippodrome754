import ctypes
import io
import os
import pathlib

import numpy
import pygame as pg

from state import State


class Camera(ctypes.Structure):
    _fields_ = [('x', ctypes.c_double), ('y', ctypes.c_double),
                ('angle', ctypes.c_double), ('height', ctypes.c_double),
                ('pitch', ctypes.c_double)]


class Screen(ctypes.Structure):
    _fields_ = [('width', ctypes.c_int), ('height', ctypes.c_int)]


class Maps(ctypes.Structure):
    _fields_ = [('colorMap', ctypes.c_char_p), ('heightMap', ctypes.c_char_p)]


libname = pathlib.Path(__file__).parent.parent.resolve() / 'ray_casting'
if os.name == 'nt':
    dll = ctypes.CDLL(str(libname) + '.dll')

else:
    dll = ctypes.CDLL(str(libname) + '.so')

dll.RayCasting.argtypes = [
    Camera, Screen, ctypes.c_double, ctypes.c_int, ctypes.c_int, Maps,
    ctypes.c_double
]
dll.RayCasting.restype = ctypes.POINTER(ctypes.POINTER(ctypes.c_int))


class Render:

    def __init__(self, screen: pg.Surface, state: State):
        self.screen = screen
        self.state = state

    def __cast(self):
        height_map = io.BytesIO()
        numpy.savetxt(height_map,
                      self.state.height_map,
                      fmt='%06x',
                      delimiter=',',
                      newline='\n')

        color_map = io.BytesIO()
        numpy.savetxt(color_map,
                      self.state.color_map,
                      fmt='%06x',
                      delimiter=',',
                      newline='\n')

        c_screen = dll.RayCasting(
            Camera(self.state.camera.get_x(), self.state.camera.get_y(),
                   self.state.camera.get_angle(), self.state.camera.get_height(),
                   self.state.camera.get_pitch()),

            Screen(self.state.SCREEN_WIDTH, self.state.SCREEN_HEIGHT),

            self.state.RAY_CASTING_DELTA_ANGLE, self.state.SCALE_HEIGHT,
            self.state.RAY_CASTING_RAY_DISTANCE,

            Maps(color_map.getvalue(), height_map.getvalue()), self.state.FOV)

        screen = [[
            int(c_screen[i][j]) for j in range(self.state.SCREEN_HEIGHT)
        ] for i in range(self.state.SCREEN_WIDTH)]

        screen_array = numpy.array(screen, dtype=int)
        
        return screen_array

    def draw(self):
        screen_array = self.__cast()
        pg.surfarray.blit_array(self.screen, screen_array)
