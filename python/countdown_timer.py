import pygame

from .state import State


class Timer:
    EVENT = pygame.USEREVENT + 1
    def __init__(self, screen: pygame.Surface, state: State, minutes: int, seconds = 0):
        self.minutes = minutes
        self.seconds = seconds
        self.screen = screen
        self.state = state
        self.font = pygame.font.SysFont(None, 100)
        self.render_text()
        
        pygame.time.set_timer(self.EVENT, 1000)

    def render_text(self):
        self.text = self.font.render("{:02d}:{:02d}".format(self.minutes, self.seconds), True, (128, 0, 0))
    
    def update(self):
        if self.seconds == 0:
            self.seconds = 59
            self.minutes -= 1
        else:
            self.seconds -= 1
        
        self.render_text()
        if self.minutes == 0 and self.seconds == 0:
            pygame.time.set_timer(self.EVENT, 0)
            self.state.lost = True
    
    def draw(self):
        rect = self.text.get_rect(topright=self.screen.get_rect().topright)
        self.screen.blit(self.text, rect)
            
        
        