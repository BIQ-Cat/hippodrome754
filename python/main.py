import pygame as pg

from map import Map
from portal import Portal
from countdown_timer import Timer
from methronome import Methronome
from vault import Vault
from scoreboard import Scoreboard
from state import State
from landscape import Landscape
from camera import Camera

def play(screen: pg.Surface, clock: pg.time.Clock, level: int, vault: Vault):
    minutes = 7 - (level % 5 - 1) // 2 + level // 5
    seconds = 30 * (level % 5 % 2)
    
    state = State(Camera())

    timer = Timer(screen, state, minutes, seconds)
    methronome = Methronome(screen, timer)
    
    if level == 0:
        portal = Portal(200, 200, state)
    else:
        portal = Portal(400, 400, state)
    
    if level == 0:
        maps = Map(2, 4)    
    else:
        maps = Map(((level // 5 + 1) * 10), ((level // 5 + 1) * 20))

    landscape = Landscape(screen, state, maps, state.MAP_RESOLUTION, portal)
    
    if level != 0:
        vault.open_vault()
    
    running = True

    vault_opened = False    
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
        methronome.update()
        
        vault.update()

        if not vault_opened and not vault.get_vault_process():
            pg.mixer.music.play(-1)
            vault_opened = True
        
        if landscape.check_win(portal):
            return True
        if state.lost:
            return False

        clock.tick(state.FPS)
        pg.display.flip()
    
    pg.mixer.music.stop()

    scoreboard = Scoreboard(level)
    scoreboard.show(screen)
    
    pg.mixer.quit()
    pg.quit()
    exit()
    

if __name__ == '__main__':
    pg.init()
    pg.mixer.init()
    pg.mixer.music.load(State.SOUND_DIR / "main.ogg") 

    screen = pg.display.set_mode((State.SCREEN_WIDTH, State.SCREEN_HEIGHT), pg.SCALED, vsync=1)
    clock = pg.time.Clock()
    vault = Vault(screen)

    win_screen = pg.image.load(State.MAP_DIR / "win.png")
    lose_screen = pg.image.load(State.MAP_DIR / "lose.png")

    level = 0

    while True:       
        pg.display.set_caption(f"Уровень {level}")
        
        if level == 0:
            pg.display.set_caption("Обучение")
            help_screen = pg.image.load(State.MAP_DIR / "shambala.png")
            screen.blit(help_screen, help_screen.get_rect(center=screen.get_rect().center))
            pg.display.flip()
            
            closed = False
            run = True
            while not closed and run:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        closed = False
                    if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                        run = False
                
            if closed:
                break
            
        
        won = play(screen, clock, level, vault)
        pg.mixer.music.stop()
        
        closed = False
        
        if won:
            vault.close_vault()
            while not closed:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        closed = True
                
                vault.update()
                pg.display.flip()
                
                if not vault.get_vault_process():
                    break
                
                clock.tick(State.FPS)
        else:
            screen.blit(lose_screen, lose_screen.get_rect(center=screen.get_rect().center))
            pg.display.flip()

            while not closed:
                for event in pg.event.get():
                    if event.type == pg.QUIT or event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                        closed = True
        
        if closed or not won:
            break
        else:
            level += 1
    
    scoreboard = Scoreboard(level)
    scoreboard.show(screen)
    
    pg.mixer.quit()
    pg.quit()
