import pygame as pg

from map import Map
from portal import Portal
from countdown_timer import Timer
from state import State
from landscape import Landscape
from camera import Camera

def play(maps: Map, minutes: int, seconds: int, screen: pg.Surface, clock: pg.time.Clock):
    state = State(Camera())

    timer = Timer(screen, state, minutes, seconds)
    portal = Portal(460, 460, state)

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
            return True
        if state.lost:
            return False

        clock.tick(state.FPS)
        pg.display.flip()

    pg.quit()
    exit()

if __name__ == '__main__':
    pg.init()

    screen = pg.display.set_mode((State.SCREEN_WIDTH, State.SCREEN_HEIGHT), pg.SCALED)
    clock = pg.time.Clock()

    win_screen = pg.image.load(State.MAP_DIR / "win.png")
    lose_screen = pg.image.load(State.MAP_DIR / "lose.png")

    level = 5

    while level != 6:
        minutes = 7 - (level - 1) // 2
        seconds = 30 * (level % 2)
        
        maps = Map(5 + (level * 5), 10 + (level * 5))
        
        won = play(maps, minutes, seconds, screen, clock)
        res_img = win_screen if won else lose_screen

        screen.blit(res_img, res_img.get_rect(center=screen.get_rect().center))
        pg.display.flip()

        closed = False

        while not closed:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    closed = True
                
                btn = pg.key.get_pressed()
                if btn[pg.K_q]:
                    closed = True
                if btn[pg.K_e]:
                    break
                
                clock.tick(State.FPS)
        
        if closed:
            break

        if won:
            level += 1
        
    pg.quit()
