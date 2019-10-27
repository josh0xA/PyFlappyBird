'''
physics.py - handles all the game physics
           - ie. movements, forces, velocity etc.

'''

from core.config import *
from core.fgame import *

try:
    xrange
except NameError:
    xrange = range # can only be applied with python2.7

def playerObjectShm(playerObjectShm):
    util = Utility()
    """oscillates the value of playerObjectShm['val'] between 8 and -8"""
    if abs(playerObjectShm['val']) == 8:
        playerObjectShm['dir'] *= -1

    if playerObjectShm['dir'] == 1:
         playerObjectShm['val'] += 1
    else:
        playerObjectShm['val'] -= 1

def ScoreViewer(score):
    util = Utility()
    scr = Screener()
    """displays score in center of screen"""
    digScore = [int(x) for x in list(str(score))]
    _totalwidth = 0 # total width of all numbers to be printed

    for digit in digScore: # iterate through the digits
        _totalwidth += FL_IMAGE_BOUNDARY['numbers'][digit].get_width()

    arrayOffsetX = (util.FL_GAME_SCREENWIDTH - _totalwidth) / 2

    for digit in digScore: # second iteration
        scr._KSCREEN.blit(FL_IMAGE_BOUNDARY['numbers'][digit], (arrayOffsetX, util.FL_GAME_SCREENHEIGHT * 0.1))
        arrayOffsetX += FL_IMAGE_BOUNDARY['numbers'][digit].get_width()


def RandomPipeGetter():
    util = Utility()
    """returns a randomly generated pipe"""
    # y of gap between upper and lower pipe
    gapperY = random.randrange(0, int(FL_BASE_Y * 0.6 - util.FL_PIPE_GAPPER))
    gapperY += int(FL_BASE_Y * 0.2)
    pipeHeight = FL_IMAGE_BOUNDARY['pipe'][0].get_height()
    pipeX = util.FL_GAME_SCREENWIDTH + 10

    return [
        {'x': pipeX, 'y': gapperY - pipeHeight},  # upper pipe
        {'x': pipeX, 'y': gapperY + util.FL_PIPE_GAPPER}, # lower pipe
    ]

def IsObjectCrashed(playerObject, _pipeUpper, _pipeLower):
    util = Utility()
    """returns True if playerObject collders with base or pipes."""
    jplayerObjectIndex = playerObject['index']
    playerObject['w'] = FL_IMAGE_BOUNDARY['playerObject'][0].get_width()
    playerObject['h'] = FL_IMAGE_BOUNDARY['playerObject'][0].get_height()

    # if playerObject crashes into ground
    if playerObject['y'] + playerObject['h'] >= FL_BASE_Y - 1:
        return [True, True]
    else:

        playerObjectRect = pygame.Rect(playerObject['x'], playerObject['y'],
                      playerObject['w'], playerObject['h'])
        pipeW = FL_IMAGE_BOUNDARY['pipe'][0].get_width()
        pipeH = FL_IMAGE_BOUNDARY['pipe'][0].get_height()

        for _pipeIterA, _pipeIterB in zip(_pipeUpper, _pipeLower):
            # upper and lower pipe rects
            uPipeRect = pygame.Rect(_pipeIterA['x'], _pipeIterA['y'], pipeW, pipeH)
            lPipeRect = pygame.Rect(_pipeIterB['x'], _pipeIterB['y'], pipeW, pipeH)

            # playerObject and upper/lower pipe hitmasks
            pHitMask = FL_HITMASK_BOUNDARY['playerObject'][jplayerObjectIndex]
            uHitmask = FL_HITMASK_BOUNDARY['pipe'][0]
            lHitmask = FL_HITMASK_BOUNDARY['pipe'][1]

            # if bird collided with upipe or lpipe
            collideA = OnPixelCollisionDetector(playerObjectRect, uPipeRect, pHitMask, uHitmask)
            collideB = OnPixelCollisionDetector(playerObjectRect, lPipeRect, pHitMask, lHitmask)

            if collideA or collideB:
                return [True, False]

    return [False, False]

def OnPixelCollisionDetector(_rectangleA, _rectangleB, _hitmaskA, _hitmaskB):
    util = Utility()
    """Checks if two objects collide and not just their rects"""
    r = _rectangleA.clip(_rectangleB)

    if r.width == 0 or r.height == 0:
        return False

    x1, y1 = r.x - _rectangleA.x, r.y - _rectangleA.y
    x2, y2 = r.x - _rectangleB.x, r.y - _rectangleB.y

    # on collision...
    for x in xrange(r.width):
        for y in xrange(r.height):
            if _hitmaskA[x1+x][y1+y] and _hitmaskB[x2+x][y2+y]:
                return True
    return False

def FlappyBirdLoadUp(movementInfo):
    util = Utility()
    scr = Screener()

    global FL_BASE_Y 
    FL_BASE_Y = util.FL_GAME_SCREENHEIGHT * 0.79

    score = playerObjectIndex = mLoopIterator = 0
    playerObjectIndexGen = movementInfo['playerObjectIndexGen']
    playerObjectx, playerObjecty = int(util.FL_GAME_SCREENWIDTH * 0.2), movementInfo['playerObjecty']

    FL_BASE_X = movementInfo['FL_BASE_X']
    baseShift = FL_IMAGE_BOUNDARY['base'].get_width() - FL_IMAGE_BOUNDARY['background'].get_width()

    # get 2 new pipes to add to _pipeUpper _pipeLower list
    newPipe1 = RandomPipeGetter()
    newPipe2 = RandomPipeGetter()

    # list of upper pipes
    _pipeUpper = [
        {'x': util.FL_GAME_SCREENWIDTH + 200, 'y': newPipe1[0]['y']},
        {'x': util.FL_GAME_SCREENWIDTH + 200 + (util.FL_GAME_SCREENWIDTH / 2), 'y': newPipe2[0]['y']},
    ]

    # list of lowerpipe
    _pipeLower = [
        {'x': util.FL_GAME_SCREENWIDTH + 200, 'y': newPipe1[1]['y']},
        {'x': util.FL_GAME_SCREENWIDTH + 200 + (util.FL_GAME_SCREENWIDTH / 2), 'y': newPipe2[1]['y']},
    ]

    pipeVelX = -4

    # playerObject velocity, max velocity, downward accleration, accleration on flap
    playerObjectVelY    =  -9   # playerObject's velocity along Y, default same as playerObjectFlapped
    playerObjectMaxVelY =  10   # max vel along Y, max descend speed
    playerObjectMinVelY =  -8   # min vel along Y, max ascend speed
    playerObjectAccY    =   1   # playerObjects downward accleration
    playerObjectRot     =  45   # playerObject's rotation
    playerObjectVelRot  =   3   # angular speed
    playerObjectRotThr  =  20   # rotation threshold
    playerObjectFlapAcc =  -9   # playerObjects speed on flapping
    playerObjectFlapped = False # True when playerObject flaps


    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if playerObjecty > -2 * FL_IMAGE_BOUNDARY['playerObject'][0].get_height():
                    playerObjectVelY = playerObjectFlapAcc
                    playerObjectFlapped = True
                    FL_SOUND_BOUNDARY['wing'].play()

        # check for crash here
        _tcrash = IsObjectCrashed({'x': playerObjectx, 'y': playerObjecty, 'index': playerObjectIndex},
                            _pipeUpper, _pipeLower)
        if _tcrash[0]:
            return {
                'y': playerObjecty,
                'groundCrash': _tcrash[1],
                'FL_BASE_X': FL_BASE_X,
                '_pipeUpper': _pipeUpper,
                '_pipeLower': _pipeLower,
                'score': score,
                'playerObjectVelY': playerObjectVelY,
                'playerObjectRot': playerObjectRot
            }

        # check for score
        playerObjectMidPos = playerObjectx + FL_IMAGE_BOUNDARY['playerObject'][0].get_width() / 2
        for pipe in _pipeUpper:
            pipeMidPos = pipe['x'] + FL_IMAGE_BOUNDARY['pipe'][0].get_width() / 2
            if pipeMidPos <= playerObjectMidPos < pipeMidPos + 4:
                score += 1
                FL_SOUND_BOUNDARY['treyway'].play()

        # playerObjectIndex FL_BASE_X change
        if (mLoopIterator + 1) % 3 == 0:
            playerObjectIndex = next(playerObjectIndexGen)
        mLoopIterator = (mLoopIterator + 1) % 30
        FL_BASE_X = -((-FL_BASE_X + 100) % baseShift)

        # rotate the playerObject
        if playerObjectRot > -90:
            playerObjectRot -= playerObjectVelRot

        # playerObject's movement
        if playerObjectVelY < playerObjectMaxVelY and not playerObjectFlapped:
            playerObjectVelY += playerObjectAccY
        if playerObjectFlapped:
            playerObjectFlapped = False

            # more rotation to cover the threshold (calculated in visible rotation)
            playerObjectRot = 45

        playerObjectHeight = FL_IMAGE_BOUNDARY['playerObject'][playerObjectIndex].get_height()
        playerObjecty += min(playerObjectVelY, FL_BASE_Y - playerObjecty - playerObjectHeight)

        # move pipes to left
        for _pipeIterA, _pipeIterB in zip(_pipeUpper, _pipeLower):
            _pipeIterA['x'] += pipeVelX
            _pipeIterB['x'] += pipeVelX

        # add new pipe when first pipe is about to touch left of screen
        if 0 < _pipeUpper[0]['x'] < 5:
            newPipe = RandomPipeGetter()
            _pipeUpper.append(newPipe[0])
            _pipeLower.append(newPipe[1])

        # remove first pipe if its out of the screen
        if _pipeUpper[0]['x'] < -FL_IMAGE_BOUNDARY['pipe'][0].get_width():
            _pipeUpper.pop(0)
            _pipeLower.pop(0)

        # draw gamesprites
        scr._KSCREEN.blit(FL_IMAGE_BOUNDARY['background'], (0,0))

        for _pipeIterA, _pipeIterB in zip(_pipeUpper, _pipeLower):
            scr._KSCREEN.blit(FL_IMAGE_BOUNDARY['pipe'][0], (_pipeIterA['x'], _pipeIterA['y']))
            scr._KSCREEN.blit(FL_IMAGE_BOUNDARY['pipe'][1], (_pipeIterB['x'], _pipeIterB['y']))

        scr._KSCREEN.blit(FL_IMAGE_BOUNDARY['base'], (FL_BASE_X, FL_BASE_Y))
        # print score so playerObject overlaps the score
        ScoreViewer(score)

        # playerObject rotation has a threshold
        visibleRot = playerObjectRotThr
        if playerObjectRot <= playerObjectRotThr:
            visibleRot = playerObjectRot
        
        playerObjectSurface = pygame.transform.rotate(FL_IMAGE_BOUNDARY['playerObject'][playerObjectIndex], visibleRot)
        scr._KSCREEN.blit(playerObjectSurface, (playerObjectx, playerObjecty))

        pygame.display.update()
        scr._KFPSCLOCK.tick(util.FPS_BUFFERING_LIMIT)


