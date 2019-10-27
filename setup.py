from distutils.core import setup
import py2exe

setup(console=['flappy_main.py', 'config.py', 'fgame.py', 'physics.py', 'animations.py'])