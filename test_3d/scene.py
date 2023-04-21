from model import *
import pygame as pg
import numpy as np

class Scene():
    r = 10;
    def __init__(self, app,front_back = -90, left_right=0, cw_ccw = 0,fb_deg = 0, lr_deg=0, cw_deg = 1):
        self.app = app
        self.front_back = front_back
        self.left_right = left_right
        self.cw_ccw = cw_ccw
        self.fb_deg = fb_deg
        self.lr_deg = lr_deg
        self.cw_deg = cw_deg
        self.objects = []
        self.load()

    def add_object(self, obj):
        self.objects.append(obj)

    def load(self):
        app = self.app
        add = self.add_object

        # n, s = 2, 2
        # for x in range(-n, n, s):
        #     for z in range(-n, n, s):
        #         add(Cube(app, pos=(x, -s, z)))
        self.cw_ccw = Scene.r
        add(Cat(app, pos=(0, 0, -10), rot = (self.front_back,self.cw_ccw,self.left_right)))

    def update(self):
        self.move()

    def returndeg(self):
        return self.cw_ccw

    def clear(self):
        self.objects = [];

    def move(self):
        keys = pg.key.get_pressed()
        # if keys[pg.K_t]:
        #     self.front_back += self.fb_deg
        # if keys[pg.K_g]:
        #     self.front_back -= self.fb_deg
        # if keys[pg.K_f]:
        #     self.left_right += self.lr_deg
        # if keys[pg.K_h]:
        #     self.left_right -= self.lr_deg
        # if keys[pg.K_r]:
        #     self.cw_ccw += self.cw_deg
        # if keys[pg.K_y]:
        #     self.cw_ccw -= self.cw_deg

        if keys[pg.K_z]:
            self.cw_ccw -= self.cw_deg*5
        if keys[pg.K_x]:
            self.cw_ccw -= self.cw_deg
        if keys[pg.K_c]:
            self.cw_ccw += self.cw_deg
        if keys[pg.K_v]:
            self.cw_ccw += self.cw_deg*5

        if self.cw_ccw > 360:
            self.cw_ccw = self.cw_ccw-360
        elif self.cw_ccw < 0:
            self.cw_ccw = self.cw_ccw+360
            
        self.objects  = [Cat(self.app, pos=(0, 0, -10), rot=(self.front_back,self.cw_ccw,self.left_right))]

    def render(self):
        for obj in self.objects:
            obj.render()