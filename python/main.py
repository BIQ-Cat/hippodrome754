import time
import numpy
import pygame as pg

from map import Map
from portal import Portal
from countdown_timer import Timer
from state import State
from landscape import Landscape
from camera import Camera

if __name__ == '__main__':
    pg.init()

    state = State(Camera())
    maps = Map()

    screen = pg.display.set_mode((state.SCREEN_WIDTH, state.SCREEN_HEIGHT), pg.SCALED)
    clock = pg.time.Clock()
    
    portal = Portal(250, 200, state)

    timer = Timer(1, screen, state)

    landscape = Landscape(screen, state, maps, state.MAP_RESOLUTION, portal)
    
    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == timer.EVENT:
                timer.update()

        state.camera.update()

        landscape.terraforming()
        landscape.update()
        landscape.render()

        timer.draw()
        
        if landscape.check_win(portal):
            print("Win")
            break

        clock.tick(state.FPS)
        pg.display.flip()

    pg.quit()
