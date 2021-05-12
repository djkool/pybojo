##
#
# Simple State
#
##

import pygame as pg
from pygame.locals import *
import logging

from djlib.game import GameState
from djlib.asset import AnimationSet

from player import Player

log = logging.getLogger(__name__)


###############################################################################
##  SimpleState

class SimpleState(GameState):


    def __init__(self):
        GameState.__init__(self)

        # Define state properties
        #
        self.player_anim = None
        self.player = None


    def initialize(self):
        """Called the first time the game is changed to this state
           during the applications lifecycle."""

        # Load animations
        self.player_anim = AnimationSet("./assets/images/guy.png",  (16, 24))
        self.player_anim.addAnim("walk_down", 0, 3)
        self.player_anim.addAnim("walk_right", 4, 7)
        self.player_anim.addAnim("walk_left", 8, 11)
        self.player_anim.addAnim("walk_up", 12, 15)
        self.player_anim.addAnim("idle", 16, 19)

        # Create Player
        self.player = Player(*self.gc.screen.get_rect().center, anim_set=self.player_anim)


    def enter(self):
        """Called every time the game is switched to this state."""
        pass


    def processInput(self):
        """Called during normal update/render period for this state
           to process it's input."""

        for e in pg.event.get():
            if e.type == QUIT:
                self.gc.quit()
            elif e.type == KEYDOWN:
                if e.key == K_ESCAPE:
                    self.gc.quit()


    def update(self):
        """Called during normal update/render period for this state
           to update it's local or game data."""

        pg.display.set_caption("%s : %f" % (self.__class__.__name__, self.gc.clock.get_fps()))

        dt = self.gc.time_step
        self.player.update(dt)


    def render(self):
        """Called during normal update/render period for this state
           to render it's data in a specific way."""

        self.gc.screen.fill((255, 255, 255))
        self.player.render(self.gc.screen)

        pg.display.flip()


    def leave(self):
        """Called whenever we switch from this state to another."""
        pass

# end SimpleState
