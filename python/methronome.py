import numpy
import pygame

from .countdown_timer import Timer

class Ball(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, timer: Timer, *groups: pygame.sprite.Group) -> None:
        super().__init__(*groups)
        
        self.timer = timer
        self.last_minute = timer.minutes
        self.first_minute = timer.minutes
        if timer.seconds == 0:
            self.last_minute -= 1
            self.first_minute -= 1
        
        self.radius = 10
        
        self.image = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA, 32)
        self.color = pygame.Color(127, 127, 127)
        self.circle = pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        
        self.rect = pygame.Rect(x, y, 2 * self.radius, 2 * self.radius)
        
        self.vel = 2
    
    def update(self, methronome_walls: pygame.sprite.Group, *args):
        self.rect = self.rect.move(self.vel, 0)
        if pygame.sprite.spritecollideany(self, methronome_walls): # type: ignore
            self.vel = -self.vel
        
        if self.timer.minutes < self.last_minute:
            self.color.update((self.color.r + 10) % 256, abs(self.color.g - 10) % 256, abs(self.color.b - 10) % 256)
            self.circle = pygame.draw.circle(self.image, self.color, self.circle.center, self.radius)
            self.last_minute = self.timer.minutes
            self.vel += numpy.sign(self.vel)
        
        if self.timer.seconds == 0 and self.timer.minutes == 0:
            self.image.fill((255, 0, 0))
        
    
    
class Wall(pygame.sprite.Sprite):
    def __init__(self, x: int, y: int, timer: Timer, *groups: pygame.sprite.Group) -> None:
        super().__init__(*groups)
        
        self.width = 5
        self.height = 60
        
        self.timer = timer
        
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill((255, 255, 255))
        
        self.rect = pygame.Rect(x, y, self.width, self.height)
    
    def update(self, *args):
        super().update()
        if self.timer.seconds == 0 and self.timer.minutes == 0:
            self.image.fill((0, 0, 255))
        
        
        

class Methronome():
    def __init__(self, screen: pygame.Surface, timer: Timer):
        self.__methronome_group = pygame.sprite.Group()
        self.__methronome_walls = pygame.sprite.Group()
        
        self.ball = Ball(40, 40, timer, self.__methronome_group)
        
        self.wall_left = Wall(30, 30, timer, self.__methronome_group, self.__methronome_walls)
        self.wall_right = Wall(200, 30, timer, self.__methronome_group, self.__methronome_walls)
        
        self.screen = screen
    
    def update(self):
        self.__methronome_group.update(self.__methronome_walls)
        self.__methronome_group.draw(self.screen)