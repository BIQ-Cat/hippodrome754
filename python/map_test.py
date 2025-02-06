import pygame as pg

from state import State
from render import Render
from camera import Camera
from map import Map

if __name__ == '__main__':
    pg.init()

    screen = pg.display.set_mode((500, 500), pg.SCALED)
    clock = pg.time.Clock()

    state = State(Camera())
    # render = Render(screen, state)

    map = Map()

    running = True
    while running:
        state.camera.update()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        # render.draw()
                
        pg.surfarray.blit_array(screen, map.get_height_map())

        clock.tick(state.FPS)
        pg.display.flip()

    pg.quit()
