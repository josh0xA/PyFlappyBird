'''
fgame.py - handles all the universal program variables

Josh Schiavone
'''
from core.config import *

class Utility(object):
    def __init__(self):
        self.FPS_BUFFERING_LIMIT = 30
        self.FL_GAME_SCREENWIDTH = 288
        self.FL_GAME_SCREENHEIGHT = 512
        self.FL_PIPE_GAPPER  = 100 # gap between upper and lower part of pipe

class Screener(object):
    _KFPSCLOCK = pygame.time.Clock()
    _KSCREEN = pygame.display.set_mode((288, 512))

FL_IMAGE_BOUNDARY, FL_SOUND_BOUNDARY, FL_HITMASK_BOUNDARY = {}, {}, {}
