__all__ = ("Button",)

import pygame

from quack.elements.rect import Rect
from quack.elements.text import Text


class Button(Rect):
    def __init__(
        self,
        pos: tuple[int, int],
        btn_text: str,
        btn_text_size: int,
        width: int,
        height: int,
        colour: tuple[int, int, int],
        *,
        btn_text_font: str = "",
        btn_text_colour: tuple[int, int, int] = (255, 255, 255),
        border_width: int = 0,
        border_radius: int = 0,
    ) -> None:
        super().__init__(
            pos,
            width,
            height,
            colour,
            border_width=border_width,
            border_radius=border_radius,
        )

        self._text: Text = Text(btn_text, btn_text_size, btn_text_font, (0, 0), colour=btn_text_colour)

    def draw(self, surface: pygame.Surface) -> None:
        self._text.center(self)

        super().draw(surface)
        self._text.draw(surface)
