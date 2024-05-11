__all__ = ("InputBox",)

import pygame

from quack.elements.rect import Rect
from quack.dispatcher import EventContext

from quack.elements.text import Text


class InputBox(Rect):
    def __init__(
        self,
        size: tuple[int, int],
        pos: tuple[int, int],
        *,
        character_limit: int = -1,
        colour: tuple[int, int, int] = (255, 255, 255),
        user_text_colour: tuple[int, int, int] = (0, 0, 0),
        user_text_size: int = 30,
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

        self._user_text = Text("", user_text_size, "", (0, 0), colour=user_text_colour)

        self.character_limit: int = character_limit

        self.on_key(self._key_cb)

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)

        self._user_text.center(self)
        self._user_text.draw(surface)

    async def _key_cb(self, ctx: EventContext) -> None:
        self._user_text.text += ctx.key_pressed

        if self._user_text.get_width() >= (self.width - 10) or (self.character_limit != -1 and len(self._user_text.text) > self.character_limit):
            self._user_text.text = self._user_text.text[:-1]
