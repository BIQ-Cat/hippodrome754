import math

import pygame as pg


class Camera:
    def __init__(self, x=-200, y=-200, 
                       height=270, 
                       angle=math.pi / 4, pitch=20, 
                       vel=3, angle_vel=0.01):
        self.x = x
        self.y = y

        self.height = height
        
        self.angle = angle
        self.pitch = pitch

        self.vel = vel
        self.angle_vel = angle_vel

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
    def get_height(self):
        return self.height
    
    def get_angle(self):
        return self.angle
    
    def get_pitch(self):
        return self.pitch

    def update(self):
        cos_a = math.cos(self.angle)
        sin_a = math.sin(self.angle)

        key = pg.key.get_pressed()
        
        if key[pg.K_w]:
            self.x += self.vel * cos_a
            self.y += self.vel * sin_a

        if key[pg.K_s]:
            self.x -= self.vel * cos_a
            self.y -= self.vel * sin_a

        if key[pg.K_a]:
            self.x += self.vel * sin_a
            self.y -= self.vel * cos_a

        if key[pg.K_d]:
            self.x -= self.vel * sin_a
            self.y += self.vel * cos_a

        if key[pg.K_j]:
            self.pitch += self.vel

        if key[pg.K_k]:
            self.pitch -= self.vel

        if key[pg.K_h]:
            self.angle -= self.angle_vel
            
        if key[pg.K_l]:
            self.angle += self.angle_vel

        if key[pg.K_n]:
            self.height += self.vel

        if key[pg.K_m]:
            self.height -= self.vel
