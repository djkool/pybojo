#!/usr/bin/env python
##
#
# Version 0.1
#
# Pectin Game Main
#
##

import os, sys
from argparse import ArgumentParser
from configparser import ConfigParser
from importlib import import_module
from traceback import print_exception
import logging
import pygame as pg

from djlib.game import GameClass

import paths

log = logging.getLogger(__name__)

LOG_FORMAT = "%(asctime)-15s [%(levelname)-8s] %(funcName)s: %(message)s"
DTIME_FORMAT = "%Y-%m-%d_%H.%M.%S"


###############################################################################
##  PectinGameApp

class PectinGameApp(GameClass):

    APP_NAME = "Game Pectin"

    def __init__(self, config=None):
        GameClass.__init__(self)

        # Global Constants
        self.SCREEN_SIZE = (800, 600)
        self.DESIRED_FPS = 30

        # Itemize Global GameClass variables for reference
        # Anything here can be accessed in a GameState by self.gc.****
        self.config = config
        self.screen = None
        self.clock = None
        self.time = 0
        self.time_step = 0.0


    def initialize(self):
        GameClass.initialize(self)

        # Init pygame
        pg.init()
        pg.font.init()

        screen_size = (self.config.getint('default', 'screen_width', fallback=self.SCREEN_SIZE[0]),
                       self.config.getint('default', 'screen_height', fallback=self.SCREEN_SIZE[1]))
        fs = self.config.getint('default', 'fullscreen', fallback=1)
        self.screen = pg.display.set_mode(screen_size, pg.FULLSCREEN | pg.HWSURFACE if fs else 0)

        self.clock = pg.time.Clock()


    def update(self):
        # Must be done before GameClass.update() so it can
        # be used by GameState this frame
        self.clock.tick(self.DESIRED_FPS)
        self.time = pg.time.get_ticks()
        self.time_step = self.clock.get_time()/1000.0

        GameClass.update(self)

    def shutdown(self):
        GameClass.shutdown(self)

        pg.font.quit()
        pg.quit()

        logging.shutdown()

    def quit(self):
        # tell systems to shut down
        self.running = False

    def caption(self):
        return PectinGameApp.APP_NAME

_APP_CLASS = PectinGameApp


# Keep app initialization code out of __main__ so
# that it can be started directly from the state modules.
def startApp(initial_state, *args, **kargs):
    parser = ArgumentParser(description='Starter sugar for pygame projects.')
    parser.add_argument('-c', '--config', default='default.cfg', help='Specify configuration file.')
    parser.add_argument('-s', '--initial-state', default=None, help="Specify initial starting state.")
    parser.add_argument('-w', '--windowed', action='store_true', help='Start in windowed mode.')

    args = parser.parse_args()

    # load Config file
    myPath = os.path.dirname(os.path.abspath(__file__))
    mainConfig = os.path.join(myPath, args.config)
    config = ConfigParser()
    config.read(mainConfig)

    # Init logging
    #logging.basicConfig(format=, level=config.get('default', 'log_level', fallback=logging.WARNING))
    root_log = logging.getLogger()
    root_log.setLevel(config.get('default', 'log_level', fallback=logging.WARNING))
    log_file = config.get('default', 'log_dir', fallback=None)
    handlers = [logging.StreamHandler()]
    if log_file:
        from datetime import datetime
        fname = "%s.%s.log" % (args.booth, datetime.now().strftime(DTIME_FORMAT))
        log_file = os.path.join(log_file, fname)
        handlers.append(logging.FileHandler(log_file))

    fmt = logging.Formatter(LOG_FORMAT)
    for h in handlers:
        h.setFormatter(fmt)
        root_log.addHandler(h)

    print("########################################################################")
    print("##", _APP_CLASS.APP_NAME)
    print("########################################################################")
    print("## Config file: %s" % mainConfig)
    print("## Log file: %s" % log_file)
    print("########################################################################")

    # Config overrides
    if args.windowed:
        log.debug("Starting in windowed mode.")
        config.set('default', 'fullscreen', '0')

    paths.loadFromConfig(config)

    # Initialize App
    log.debug("Initializing %s", _APP_CLASS.__name__)
    app = _APP_CLASS(config)
    app.initialize()

    # Check config for initial_state overrides
    if not initial_state:
        stateclass_name = args.initial_state if args.initial_state else config.get('default', 'initial_state', fallback="loading.LoadingState")
        if stateclass_name:
            try:
                # Attempt to import the specified state module
                sc_split = stateclass_name.rindex('.')
                if sc_split != -1:
                    mod_name = paths.STATES_PATH.lstrip("./") + "." + stateclass_name[:sc_split]
                    mod = import_module(mod_name)
                    initial_state = mod.__dict__.get(stateclass_name[sc_split+1:])
            except Exception as e:
                log.error("Config contains invalid initial state module.class: %s", stateclass_name)
                log.exception(e)

    log.debug("Entering initial state: %s", initial_state.__name__)
    app.changeState(initial_state)

    # Main App Loop
    log.debug("Entering Main Loop")
    while app.running:
        app.update()

    log.debug("Entering Cleanup")
    # Cleanup
    app.shutdown()


###############################################################################
##  Main

if __name__ == "__main__":
    # Allow arguments to dictate initial state
    try:
        startApp(None)
    except Exception as e:
        logging.exception(e)

###############################################################################
