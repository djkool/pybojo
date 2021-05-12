##
#
# Loading State
#
##

import pygame
from pygame.locals import *
import logging
from random import randint

from djlib.game import GameState

log = logging.getLogger(__name__)



###############################################################################
##  LoadingState

class LoadingState(GameState):

    RECT_COLOR = pygame.Color(255, 255, 255)

    MAX_SPEED = 50

    def __init__(self):
        GameState.__init__(self)

        # Define state properties
        #
        self.rect = None

    def initialize(self):
        """Called the first time the game is changed to this state
           during the applications lifecycle."""

        # Initialize state properties
        #
        self.rect = pygame.Rect(0, 0, 100, 100)
        self.rect.center = (self.gc.screen.get_width() // 2, self.gc.screen.get_height() // 2)
        self.rect_vel = (randint(-self.MAX_SPEED, self.MAX_SPEED), randint(-self.MAX_SPEED, self.MAX_SPEED))


    def enter(self):
        """Called every time the game is switched to this state."""
        pass


    def processInput(self):
        """Called during normal update/render period for this state
           to process it's input."""

        for e in pygame.event.get():
            if e.type == QUIT:
                self.gc.quit()


    def update(self):
        """Called during normal update/render period for this state
           to update it's local or game data."""

        pygame.display.set_caption("%s : %f" % (self.__class__.__name__, self.gc.clock.get_fps()))

        dt = self.gc.time_step
        self.rect.move_ip(self.rect_vel[0] * dt, self.rect_vel[1] * dt)
        if not self.gc.screen.get_rect().contains(self.rect):
            self.rect.clamp_ip(self.gc.screen.get_rect())
            # randomize new velocity
            self.rect_vel = (randint(-self.MAX_SPEED, self.MAX_SPEED), randint(-self.MAX_SPEED, self.MAX_SPEED))


    def render(self):
        """Called during normal update/render period for this state
           to render it's data in a specific way."""
        self.gc.screen.fill((0,0,0))
        pygame.draw.rect(self.gc.screen, self.RECT_COLOR, self.rect)
        pygame.display.flip()


    def leave(self):
        """Called whenever we switch from this state to another."""
        pass

# end LoadingState
