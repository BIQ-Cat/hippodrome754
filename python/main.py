import math
import pygame as pg

from state import State
from render import Render

if __name__ == '__main__':
    pg.init()

    screen = pg.display.set_mode((800, 450), pg.SCALED)
    clock = pg.time.Clock()

    state = State()
    render = Render(screen, state)

    vel = 3
    angle_vel = 0.01

    running = True
    while running:
        cos_a = math.cos(state.camera["angle"])
        sin_a = math.sin(state.camera["angle"])

        pressed_key = pg.key.get_pressed()
        if pressed_key[pg.K_j]:
            state.camera["pitch"] += vel
        if pressed_key[pg.K_DOWN]:
            state.camera["pitch"] -= vel

        if pressed_key[pg.K_k]:
            state.camera["angle"] -= angle_vel
        if pressed_key[pg.K_RIGHT]:
            state.camera["angle"] += angle_vel

        if pressed_key[pg.K_h]:
            state.camera["height"] += vel
        if pressed_key[pg.K_l]:
            state.camera["height"] -= vel

        if pressed_key[pg.K_w]:
            state.camera["x"] += vel * cos_a
            state.camera["y"] += vel * sin_a
        if pressed_key[pg.K_s]:
            state.camera["x"] -= vel * cos_a
            state.camera["y"] -= vel * sin_a
        if pressed_key[pg.K_a]:
            state.camera["x"] += vel * sin_a
            state.camera["y"] -= vel * cos_a
        if pressed_key[pg.K_d]:
            state.camera["x"] -= vel * sin_a
            state.camera["y"] += vel * cos_a

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        render.draw()

        clock.tick(state.FPS)
        pg.display.flip()

    pg.quit()
