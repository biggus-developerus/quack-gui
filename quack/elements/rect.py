__all__ = ("Rect",)

from typing import Optional

import pygame

from quack.abc import Element


class Rect(Element):
    def __init__(
        self,
        pos: tuple[int, int],
        width: int,
        height: int,
        colour: tuple[int, int, int],
        *,
        border_width: int = 0,
        border_radius: int = 0,
    ) -> None:
        super().__init__(pos)

        self.width: int = width
        self.height: int = height

        self.colour: tuple[int, int, int] = colour

        self.border_width: int = border_width
        self.border_radius: int = border_radius

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(
            surface,
            self.colour,
            (*self.pos, self.width, self.height),
            width=self.border_width,
            border_radius=self.border_radius,
        )

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(*self.pos, self.width, self.height)

    def get_size(self) -> tuple[int, int]:
        return (self.width, self.height)
