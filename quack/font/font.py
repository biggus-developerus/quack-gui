__all__ = (
    "Font",
    "FontProperty",
)

import re

import pygame
from aenum import IntFlag

from quack.font.font_manager import FontManager

BPATT = re.compile(r"\*\*(.*?)\*\*")
STHRPATT = re.compile(r"~~(.*?)~~")
UNDPATT = re.compile(r"__(.*?)__")
ITPATT = re.compile(r"(?<!_)_(.*?)(?!_)")


class FontProperty(IntFlag):
    NONE = 0
    BOLD = 1 << 2
    STRIKETHROUGH = 1 << 3
    UNDERLINE = 1 << 4
    ITALIC = 1 << 5


class Font:
    @staticmethod
    def get_text_properties(text: str) -> "FontProperty":
        bold_match = len(BPATT.findall(text)) > 0
        underline_match = len(UNDPATT.findall(text)) > 0
        strikethrough_match = len(STHRPATT.findall(text)) > 0
        italic_match = len(ITPATT.findall(text)) > 0

        result = FontProperty.NONE

        if bold_match:
            result |= FontProperty.BOLD
        if strikethrough_match:
            result |= FontProperty.STRIKETHROUGH
        if underline_match:
            result |= FontProperty.UNDERLINE
        if italic_match:
            result |= FontProperty.ITALIC

        return result

    @staticmethod
    def remove_markers_from_text(text: str, properties: "FontProperty") -> str:
        res_text = text
        if properties & FontProperty.BOLD:
            res_text = BPATT.sub(r"\1", res_text)
        if properties & FontProperty.STRIKETHROUGH:
            res_text = STHRPATT.sub(r"\1", res_text)
        if properties & FontProperty.UNDERLINE:
            res_text = UNDPATT.sub(r"\1", res_text)
        if properties & FontProperty.ITALIC:
            res_text = ITPATT.sub(r"\1", res_text)

        return res_text

    def __init__(self, font_name: str, font_size: int, *, font_properties: FontProperty = FontProperty.NONE) -> None:
        self.font_name: str = font_name
        self.font_size: int = font_size
        self.font_properties: FontProperty = font_properties
        self._pfont: pygame.font.Font = pygame.font.Font(FontManager.get_font(font_name), font_size)

        if font_properties & FontProperty.BOLD:
            self._pfont.set_bold(True)
        if font_properties & FontProperty.STRIKETHROUGH:
            self._pfont.set_strikethrough(True)
        if font_properties & FontProperty.UNDERLINE:
            self._pfont.set_underline(True)
        if font_properties & FontProperty.ITALIC:
            self._pfont.set_italic(True)

    def make_surface(self, text: str, antialias: bool = 1, colour: tuple[int, int, int] = (255, 255, 255)) -> None:
        return self._pfont.render(self.remove_markers_from_text(text, self.font_properties), antialias, colour)
