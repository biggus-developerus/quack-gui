__all__ = ("ElementManager",)

from quack.abc import Element
from quack.elements import Rect, Text
from quack.font import FontManager


class ElementManager:
    def __init__(self) -> None:
        self._elements: dict[str, Element] = {}

    def get_elements(self) -> list[Element]:
        return list(self._elements.values())

    def add_inputbox(
        self,
        inputbox_name: str,
        w_and_h: tuple[int, int],
        position: tuple[int, int],
        *,
        colour: tuple[int, int, int] = (255, 255, 255),
        border_width: int = 3,
        border_radius=50,
    ) -> Rect:
        self._elements[inputbox_name] = (
            rect := Rect(position, *w_and_h, colour=colour, border_width=border_width, border_radius=border_radius)
        )
        return rect

    def add_text(
        self,
        text_name: str,
        text: str,
        size: int,
        pos: tuple[int, int],
        *,
        font: str = FontManager.get_default_font(),
        colour: tuple[int, int, int] = (255, 255, 255),
    ) -> Text:
        self._elements[text_name] = (text := Text(text, size, font, pos, colour=colour))
        return text
