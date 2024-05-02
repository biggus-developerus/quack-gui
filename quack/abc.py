__all__ = ("Drawable",)

from abc import ABC, abstractmethod

import pygame


class Drawable(ABC):
    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None: ...
