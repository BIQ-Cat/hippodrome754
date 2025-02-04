import pygame as pg

from map import Map
from state import State
from render import Render
from camera import Camera

if __name__ == '__main__':
    pg.init()

    state = State(Camera())
    maps = Map()

    screen = pg.display.set_mode((state.SCREEN_WIDTH, state.SCREEN_HEIGHT), pg.SCALED)
    clock = pg.time.Clock()

    render = Render(screen, state, maps)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        state.camera.update()
        render.draw()

        clock.tick(state.FPS)
        pg.display.flip()

    pg.quit()
