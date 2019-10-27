'''
animations.py - handles all the games animation functions
                and allows for graphics to be displayed
'''

from core.config import *
from core.fgame import *
from core.physics import *

def WelcomeAnimatorGetter():
    """Shows welcome screen animation of flappy bird"""
    util = Utility()
    scr = Screener()

    global FL_BASE_Y 
    FL_BASE_Y = util.FL_GAME_SCREENHEIGHT * 0.79
    # index of playerObject to blit on screen
    playerObjectIndex = 0
    playerObjectIndexGen = cycle([0, 1, 2, 1])
    # iterator used to change playerObjectIndex after every 5th iteration
    mLoopIterator = 0

    playerObjectx = int(util.FL_GAME_SCREENWIDTH * 0.2)
    playerObjecty = int((util.FL_GAME_SCREENHEIGHT - FL_IMAGE_BOUNDARY['playerObject'][0].get_height()) / 2)

    messagex = int((util.FL_GAME_SCREENWIDTH - FL_IMAGE_BOUNDARY['message'].get_width()) / 2)
    messagey = int(util.FL_GAME_SCREENHEIGHT * 0.12)

    FL_BASE_X = 0
    # amount by which base can maximum shift to left
    baseShift = FL_IMAGE_BOUNDARY['base'].get_width() - FL_IMAGE_BOUNDARY['background'].get_width()

    # playerObject shm for up-down motion on welcome screen
    playerObjectShmVals = {'val': 0, 'dir': 1}

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                # make first flap sound and return values for FlappyBirdLoadUp
                FL_SOUND_BOUNDARY['wing'].play()
                return {
                    'playerObjecty': playerObjecty + playerObjectShmVals['val'],
                    'FL_BASE_X': FL_BASE_X,
                    'playerObjectIndexGen': playerObjectIndexGen,
                }

        # adjust playerObjecty, playerObjectIndex, FL_BASE_X
        if (mLoopIterator + 1) % 5 == 0:
            playerObjectIndex = next(playerObjectIndexGen)
        mLoopIterator = (mLoopIterator + 1) % 30
        FL_BASE_X = -((-FL_BASE_X + 4) % baseShift)
        playerObjectShm(playerObjectShmVals)

        # draw gamesprites
        scr._KSCREEN.blit(FL_IMAGE_BOUNDARY['background'], (0,0))
        scr._KSCREEN.blit(FL_IMAGE_BOUNDARY['playerObject'][playerObjectIndex],
                    (playerObjectx, playerObjecty + playerObjectShmVals['val']))
        scr._KSCREEN.blit(FL_IMAGE_BOUNDARY['message'], (messagex, messagey))
        scr._KSCREEN.blit(FL_IMAGE_BOUNDARY['base'], (FL_BASE_X, FL_BASE_Y))

        pygame.display.update()
        scr._KFPSCLOCK.tick(util.FPS_BUFFERING_LIMIT)

def OnGameOverTriggerAnimation(crashInfo):
    util = Utility()
    scr = Screener()
    """crashes the playerObject down ans shows gameover image"""
    score = crashInfo['score']
    playerObjectx = util.FL_GAME_SCREENWIDTH * 0.2
    playerObjecty = crashInfo['y']
    playerObjectHeight = FL_IMAGE_BOUNDARY['playerObject'][0].get_height()
    playerObjectVelY = crashInfo['playerObjectVelY']
    playerObjectAccY = 2
    playerObjectRot = crashInfo['playerObjectRot']
    playerObjectVelRot = 7

    FL_BASE_X = crashInfo['FL_BASE_X']

    _pipeUpper, _pipeLower = crashInfo['_pipeUpper'], crashInfo['_pipeLower']

    # play hit and die sounds
    FL_SOUND_BOUNDARY['hit'].play()
    if not crashInfo['groundCrash']:
        FL_SOUND_BOUNDARY['die'].play()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playerObjecty + playerObjectHeight >= FL_BASE_Y - 1:
                    return

        # playerObject y shift
        if playerObjecty + playerObjectHeight < FL_BASE_Y - 1:
            playerObjecty += min(playerObjectVelY, FL_BASE_Y - playerObjecty - playerObjectHeight)

        # playerObject velocity change
        if playerObjectVelY < 15:
            playerObjectVelY += playerObjectAccY

        # rotate only when it's a pipe crash
        if not crashInfo['groundCrash']:
            if playerObjectRot > -90:
                playerObjectRot -= playerObjectVelRot

        # draw gamesprites
        scr._KSCREEN.blit(FL_IMAGE_BOUNDARY['background'], (0,0))

        for _pipeIterA, _pipeIterB in zip(_pipeUpper, _pipeLower):
            scr._KSCREEN.blit(FL_IMAGE_BOUNDARY['pipe'][0], (_pipeIterA['x'], _pipeIterA['y']))
            scr._KSCREEN.blit(FL_IMAGE_BOUNDARY['pipe'][1], (_pipeIterB['x'], _pipeIterB['y']))

        scr._KSCREEN.blit(FL_IMAGE_BOUNDARY['base'], (FL_BASE_X, FL_BASE_Y))
        ScoreViewer(score)

        playerObjectSurface = pygame.transform.rotate(FL_IMAGE_BOUNDARY['playerObject'][1], playerObjectRot)
        scr._KSCREEN.blit(playerObjectSurface, (playerObjectx,playerObjecty))
        scr._KSCREEN.blit(FL_IMAGE_BOUNDARY['gameover'], (50, 180))

        scr._KFPSCLOCK.tick(util.FPS_BUFFERING_LIMIT)
        pygame.display.update()
