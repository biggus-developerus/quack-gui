from .abc import *
from .app import *
from .dispatcher import *
from .element_manager import *
from .elements import *
from .font import *


def init() -> None:
    import pygame

    pygame.init()
    FontManager.init()
