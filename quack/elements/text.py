__all__ = ("Text",)

from typing import Any, Optional

import pygame

from quack.element import Element
from quack.font import Font, FontManager, FontProperty


class Text(Element):
    _dynamic_attrs: list[str] = [
        "text",
        "size",
        "font_properties",
        "pos",
        "colour",
    ]

    def __init__(
        self,
        text: str,
        size: int,
        font: str,
        pos: tuple[int, int],
        *,
        colour: tuple[int, int, int] = (255, 255, 255),
    ) -> None:
        super().__init__(pos, colour)

        self.text: str = text
        self.size: int = size
        self.font_properties: FontProperty = Font.get_text_properties(text)

        self.font: Font = Font(
            FontManager.get_font(font) or FontManager.get_default_font(),
            size,
            font_properties=self.font_properties,
        )

        self._text_surface: Optional[pygame.Surface] = None

    def draw(self, surface: pygame.Surface) -> None:
        if self._text_surface:
            surface.blit(self._text_surface, self.pos)
            return

        self._text_surface = self.font.make_surface(self.text, 1, self.colour)
        surface.blit(self._text_surface, self.pos)

    def get_rect(self) -> pygame.Rect:
        if not self._text_surface:
            self._text_surface = self.font.make_surface(self.text, 1, self.colour)

        return pygame.Rect((*self.pos, *self._text_surface.get_size()))

    def __setattr__(self, name: str, value: Any) -> None:
        if name in self._dynamic_attrs:
            self._text_surface = None

        return super().__setattr__(name, value)
