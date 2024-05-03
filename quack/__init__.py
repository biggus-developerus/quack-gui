from .abc import *
from .app import *
from .elements import *
from .element_manager import *
from .font import *
from .dispatcher import *

def init() -> None:
    import pygame

    pygame.init()
    FontManager.init()
