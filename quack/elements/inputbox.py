__all__ = ("InputBox",)

import pygame

from quack.elements.rect import Rect

# from quack.elements.text import Text


class InputBox(Rect):
    def __init__(
        self,
        size: tuple[int, int],
        pos: tuple[int, int],
        *,
        # place_holder_text: str = "",
        # place_holder_text_size: int = 10,
        # place_holder_text_colour: tuple[int, int, int] = (0, 0, 0),
        # place_holder_text_font: str = "",
        colour: tuple[int, int, int] = (255, 255, 255),
        border_width: int = 0,
        border_radius: int = 0,
    ) -> None:
        super().__init__(
            pos,
            *size,
            colour=colour,
            border_width=border_width,
            border_radius=border_radius,
        )

        self.is_activated: bool = False

        # self.text = Text(
        #     place_holder_text,
        #     place_holder_text_size,
        #     place_holder_text_font,
        #     pos,
        #     colour=place_holder_text_colour,
        # )

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        # self.text.draw(surface)
