__all__ = ("Element",)

from abc import ABC, abstractmethod

import pygame


class Element(ABC):
    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None: ...
