from .app import *
from .font import *


def init() -> None:
    import pygame

    pygame.init()
    FontManager.init()
