__all__ = ("ElementManager",)

from abc import ABC

from quack.element import Element
from quack.elements import InputBox, Rect, Text
from quack.font import FontManager


class ElementManager(
    ABC
):  # SOB X50 MUST BE INHERITED BY APP AND APP ALONE, OR ELSE Element WOULD GET CONFUSEDDDD!!!!!!!!!!!!!
    def __init__(self) -> None:
        self._elements: list[Element] = []

    def get_elements(self) -> list[Element]:
        return self._elements

    def add_element(self, element: Element) -> None:
        self._elements.append(element)
        element.set_app(self)

    def remove_element(self, element: Element) -> None:
        self._elements.remove(element)

    def add_rect(
        self,
        w_and_h: tuple[int, int],
        pos: tuple[int, int] = (0, 0),
        *,
        colour: tuple[int, int, int] = (255, 255, 255),
        border_width: int = 0,
        border_radius=0,
    ) -> Rect:
        self._elements.append(
            rect := Rect(pos, *w_and_h, colour=colour, border_width=border_width, border_radius=border_radius)
        )
        rect.set_app(self)
        return rect

    def add_text(
        self,
        text: str,
        size: int,
        pos: tuple[int, int] = (0, 0),
        *,
        font: str = FontManager.get_default_font(),
        colour: tuple[int, int, int] = (255, 255, 255),
    ) -> Text:
        self._elements.append(text_element := Text(text, size, font, pos, colour=colour))
        text_element.set_app(self)

        return text_element

    def add_inputbox(
        self,
        size: tuple[int, int],
        pos: tuple[int, int] = (0, 0),
        *,
        # place_holder_text: str = "",
        # place_holder_text_size: int = 10,
        # place_holder_text_colour: tuple[int, int, int] = (0, 0, 0),
        colour: tuple[int, int, int] = (255, 255, 255),
        border_width: int = 0,
        border_radius: int = 0,
    ) -> InputBox:
        inputbox = InputBox(
            size,
            pos,
            # place_holder_text=place_holder_text,
            # place_holder_text_size=place_holder_text_size,
            # place_holder_text_colour=place_holder_text_colour,
            colour=colour,
            border_width=border_width,
            border_radius=border_radius,
        )

        self._elements.append(inputbox)
        inputbox.set_app(self)

        return inputbox
