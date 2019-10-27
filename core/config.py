'''
config.py - all the universal debugging variables
          - handles OS functions
'''

from itertools import cycle
import sys
import os
import pygame
import random
from pygame.locals import *

class FConfig:

    # Handling
    FL_ERROR_CODE_STANDARD = -1
    FL_SUCCCESS_CODE_STANDARD = 0
    FL_CURRENT_GAME_RUNNING = False
    FL_PYGAME_WINDOW_ACTIVE = False

    # OS Handlers
    FL_OSYSTEM_UNIX_LINUX = False
    FL_OSYSTEM_DARWIN = False
    FL_OSYSTEM_WIN32_64 = False

    # Game rendering args
    FL_INGAME_FPS_RATE = 30
    FL_GAME_SCREEN_WIDTH = 288
    FL_GAME_SCREEN_HEIGHT = 512
    FL_PIPE_GAPPER = 100

class Platform(object):
    def GetOperatingSystemDescriptor(self):
        flg = FConfig()
        if sys.platform == "win32" or sys.platform == "win64":
            flg.FL_OSYSTEM_WIN32_64 = True
            print("OS: WINDOWS")

        if sys.platform == "darwin": 
            flg.FL_OSYSTEM_DARWIN = True
            print("OS: UNIX/OSX")

        else:
            sys.exit(flg.FL_ERROR_CODE_STANDARD)


