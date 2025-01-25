import pygame as pg

from state import State
from render import Render


if __name__ == '__main__':
    pg.init()

    screen = pg.display.set_mode((800, 450), pg.SCALED)
    clock = pg.time.Clock()

    state = State()
    render = Render(screen, state)

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        render.draw()
        
        clock.tick(state.FPS)
        pg.display.flip()

    pg.quit()
