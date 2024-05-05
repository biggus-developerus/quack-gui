__all__ = ("ElementManager",)

from quack.element import Element
from quack.elements import Rect, Text
from quack.font import FontManager


class ElementManager:
    def __init__(self) -> None:
        self._elements: list[Element] = []

    def get_elements(self) -> list[Element]:
        return self._elements

    def add_element(self, element: Element) -> None:
        self._elements.append(element)

    def remove_element(self, element: Element) -> None:
        self._elements.remove(element)

    def add_rect(
        self,
        w_and_h: tuple[int, int],
        position: tuple[int, int],
        *,
        colour: tuple[int, int, int] = (255, 255, 255),
        border_width: int = 0,
        border_radius=0,
    ) -> Rect:
        self._elements.append(
            rect := Rect(position, *w_and_h, colour=colour, border_width=border_width, border_radius=border_radius)
        )
        return rect

    def add_text(
        self,
        text: str,
        size: int,
        pos: tuple[int, int],
        *,
        font: str = FontManager.get_default_font(),
        colour: tuple[int, int, int] = (255, 255, 255),
    ) -> Text:
        self._elements.append(text := Text(text, size, font, pos, colour=colour))
        return text
