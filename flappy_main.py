"""
    FlappyBird - Josh Schiavone
        For: Mr. Hofstatter

    I've decided to keep the source code for this project
    into one file for debugging purposes. 

    PS: I only implemented "one level" due to the fact that I want 
    this project to be as close to the original flappy bird game so I only
    added one, infinite level. 

"""
from core.config import *
from core.fgame import *
from core.physics import *
from core.animations import *

FL_BIRD_BUFFER = (
    # red bird
    (
        'dependencies/gamesprites/redbird-upflap.png',
        'dependencies/gamesprites/redbird-midflap.png',
        'dependencies/gamesprites/redbird-downflap.png',
    ),
    # blue bird
    (
        'dependencies/gamesprites/bluebird-upflap.png',
        'dependencies/gamesprites/bluebird-midflap.png',
        'dependencies/gamesprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'dependencies/gamesprites/yellowbird-upflap.png',
        'dependencies/gamesprites/yellowbird-midflap.png',
        'dependencies/gamesprites/yellowbird-downflap.png',
    ),
)

# list of backgrounds
FL_BACKGROUND_BUFFER = (
    'dependencies/gamesprites/background-day.png',
    'dependencies/gamesprites/background-night.png',
)

# list of pipes
FL_PIPE_BUFFER = (
    'dependencies/gamesprites/pipe-green.png',
    'dependencies/gamesprites/pipe-red.png',
)


def HitmaskGetter(image):
    util = Utility()
    """return s a hitmask using an image's alpha."""
    mask = []
    for x in xrange(image.get_width()):
        mask.append([])
        for y in xrange(image.get_height()):
            mask[x].append(bool(image.get_at((x,y))[3]))
    return mask

def FlappyBirdMain():
    util = Utility()
    pltf = Platform()
    pltf.GetOperatingSystemDescriptor()

    pygame.init() 
    pygame.display.set_caption('Josh Schiavone - Flappy Bird')


    # numbers gamesprites for score display
    FL_IMAGE_BOUNDARY['numbers'] = (
        pygame.image.load('dependencies/gamesprites/0.png').convert_alpha(),
        pygame.image.load('dependencies/gamesprites/1.png').convert_alpha(),
        pygame.image.load('dependencies/gamesprites/2.png').convert_alpha(),
        pygame.image.load('dependencies/gamesprites/3.png').convert_alpha(),
        pygame.image.load('dependencies/gamesprites/4.png').convert_alpha(),
        pygame.image.load('dependencies/gamesprites/5.png').convert_alpha(),
        pygame.image.load('dependencies/gamesprites/6.png').convert_alpha(),
        pygame.image.load('dependencies/gamesprites/7.png').convert_alpha(),
        pygame.image.load('dependencies/gamesprites/8.png').convert_alpha(),
        pygame.image.load('dependencies/gamesprites/9.png').convert_alpha()
    )

    # game over sprite
    FL_IMAGE_BOUNDARY['gameover'] = pygame.image.load('dependencies/gamesprites/gameover.png').convert_alpha()
    # message sprite for welcome screen
    FL_IMAGE_BOUNDARY['message'] = pygame.image.load('dependencies/gamesprites/message.png').convert_alpha()
    # base (ground) sprite
    FL_IMAGE_BOUNDARY['base'] = pygame.image.load('dependencies/gamesprites/base.png').convert_alpha()
    
    if 'win' in sys.platform:
        soundExt = '.wav'
    else:
        soundExt = '.ogg'

    FL_SOUND_BOUNDARY['die']    = pygame.mixer.Sound('dependencies/audio/die' + soundExt)
    FL_SOUND_BOUNDARY['hit']    = pygame.mixer.Sound('dependencies/audio/hit' + soundExt)
    FL_SOUND_BOUNDARY['point']  = pygame.mixer.Sound('dependencies/audio/point' + soundExt)
    FL_SOUND_BOUNDARY['swoosh'] = pygame.mixer.Sound('dependencies/audio/swoosh' + soundExt)
    FL_SOUND_BOUNDARY['wing']   = pygame.mixer.Sound('dependencies/audio/wing' + soundExt)
    FL_SOUND_BOUNDARY['treyway']   = pygame.mixer.Sound('dependencies/audio/treyway' + soundExt)

    while True:
        # select random background gamesprites
        randBg = random.randint(0, len(FL_BACKGROUND_BUFFER) - 1)
        FL_IMAGE_BOUNDARY['background'] = pygame.image.load(FL_BACKGROUND_BUFFER[randBg]).convert()

        # select random playerObject gamesprites
        randplayerObject = random.randint(0, len(FL_BIRD_BUFFER) - 1)
        FL_IMAGE_BOUNDARY['playerObject'] = (
            pygame.image.load(FL_BIRD_BUFFER[randplayerObject][0]).convert_alpha(),
            pygame.image.load(FL_BIRD_BUFFER[randplayerObject][1]).convert_alpha(),
            pygame.image.load(FL_BIRD_BUFFER[randplayerObject][2]).convert_alpha(),
        )

        # select random pipe gamesprites
        pipeindex = random.randint(0, len(FL_PIPE_BUFFER) - 1)
        FL_IMAGE_BOUNDARY['pipe'] = (
            pygame.transform.flip(
                pygame.image.load(FL_PIPE_BUFFER[pipeindex]).convert_alpha(), False, True),
            pygame.image.load(FL_PIPE_BUFFER[pipeindex]).convert_alpha(),
        )

        # hismask for pipes
        FL_HITMASK_BOUNDARY['pipe'] = (
            HitmaskGetter(FL_IMAGE_BOUNDARY['pipe'][0]),
            HitmaskGetter(FL_IMAGE_BOUNDARY['pipe'][1]),
        )

        # hitmask for playerObject
        FL_HITMASK_BOUNDARY['playerObject'] = (
            HitmaskGetter(FL_IMAGE_BOUNDARY['playerObject'][0]),
            HitmaskGetter(FL_IMAGE_BOUNDARY['playerObject'][1]),
            HitmaskGetter(FL_IMAGE_BOUNDARY['playerObject'][2]),
        )
        movementInfo = WelcomeAnimatorGetter()
        crashInfo = FlappyBirdLoadUp(movementInfo)
        OnGameOverTriggerAnimation(crashInfo)


if __name__ == '__main__':
    FlappyBirdMain()