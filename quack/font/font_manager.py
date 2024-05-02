__all__ = ("FontManager",)

from typing import Optional

import pygame


class FontManager:
    _sys_fonts: dict[str, str] = {}  # name: path

    @classmethod
    def init(cls) -> bool:
        for font in pygame.font.get_fonts():
            if font_path := pygame.font.match_font(font):
                cls._sys_fonts[font] = font_path

    @classmethod
    def add_font(cls, name: str, path: str) -> None:
        cls._sys_fonts[name] = path

    @classmethod
    def get_font(cls, name: str) -> Optional[str]:
        return cls._sys_fonts.get(name, None)

    @classmethod
    def get_default_font(cls) -> str:
        return pygame.font.get_default_font()
