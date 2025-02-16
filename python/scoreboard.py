import os
import time

import pygame


class Scoreboard:
    def __init__(self, level: int):
        self.new_score = level
        self.get_high_score()
        
        self.font = pygame.font.SysFont(None, 100)
        self.text = f"Лучший результат: {self.high_score}"
        
    def get_high_score(self):
        if not os.path.exists("score.txt"):
            self.high_score = 0
        else:
            with open("score.txt") as f:
                self.high_score = int(f.read())
        
        if self.new_score > self.high_score:
            self.high_score = self.new_score
            with open("score.txt", "w") as f:
                f.write(str(self.high_score))
        
        
            
    def draw(self, screen: pygame.Surface):
        surf = self.font.render(self.text, True, (0, 255, 0))
        screen.blit(surf, surf.get_rect(center=screen.get_rect().center))
    
    def show(self, display: pygame.Surface):
        self.draw(display)
        pygame.display.flip()
        
        time.sleep(3)