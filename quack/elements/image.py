__all__ = ("Image",)

from io import BytesIO
from typing import Optional, Union

import pygame
from PIL import Image as pil_image

from quack.element import Element


class Image(Element):
    def __init__(self, path_or_data: Union[str, bytes], pos: tuple[int, int]) -> None:
        super().__init__(pos)

        img_data: bytes

        if isinstance(path_or_data, str):
            with open(path_or_data, "rb") as f:
                img_data = f.read()
        else:
            img_data = path_or_data

        self._pil_img: pil_image.Image = pil_image.open(BytesIO(img_data))
        self._pimgsuface: Optional[pygame.Surface] = None

    def make_img_surface(self) -> pygame.Surface:
        return pygame.image.frombuffer(self._pil_img.tobytes(), self._pil_img.size, self._pil_img.mode)

    def draw(self, surface: pygame.Surface) -> None:
        if not self._pimgsuface:
            self._pimgsuface = self.make_img_surface()

        surface.blit(self._pimgsuface, self.pos)

    def get_rect(self) -> pygame.Rect:
        if not self._pimgsuface:
            self._pimgsuface = self.make_img_surface()

        return self._pimgsuface.get_rect()

    def resize(self, width: int, height: int) -> None:
        self._pimgsuface = None
        self._pil_img = self._pil_img.resize((width, height))

    def set_alpha(self, alpha: int) -> None:
        if not self._pimgsuface:
            self._pimgsuface = self.make_img_surface()

        self._pimgsuface.set_alpha(alpha)
