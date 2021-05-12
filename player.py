##
#
# Player class
#
##


import pygame as pg
from pygame.locals import *
from djlib.asset import Animator
from djlib.primitives import Entity, Point


class Player(Entity):

    WALK_SPEED = 3

    def __init__(self, x, y, anim_set):
        Entity.__init__(self, Point(x, y))
        self.anim = Animator(anim_set, Animator.MODE_LOOP, 15.0)


    def update(self, dt):

        # Only update player anim with actual movement
        k = pg.key.get_pressed()
        if k[K_w]:
            self.pos.y -= Player.WALK_SPEED
            self.anim.setAnim("walk_up")
            self.anim.update(dt)
        elif k[K_s]:
            self.pos.y += Player.WALK_SPEED
            self.anim.setAnim("walk_down")
            self.anim.update(dt)
        if k[K_a]:
            self.pos.x -= Player.WALK_SPEED
            self.anim.setAnim("walk_left")
            self.anim.update(dt)
        elif k[K_d]:
            self.pos.x += Player.WALK_SPEED
            self.anim.setAnim("walk_right")
            self.anim.update(dt)


    def render(self, surf):
        screen_pos = (self.pos.x, self.pos.y)
        self.anim.render(surf, screen_pos)
