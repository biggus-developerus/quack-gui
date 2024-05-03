__all__ = ("Rect",)

import pygame

from quack.abc import Drawable


class Rect(Drawable):
    def __init__(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        colour: tuple[int, int, int],
        *,
        border_width: int = 0,
        border_radius: int = 0,
    ) -> None:
        self.x: int = x
        self.y: int = y

        self.width: int = width
        self.height: int = height

        self.colour: tuple[int, int, int] = colour

        self.border_width: int = border_width
        self.border_radius: int = border_radius

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface,
            self.colour,
            (self.x, self.y, self.width, self.height),
            width=self.border_width,
            border_radius=self.border_radius,
        )
