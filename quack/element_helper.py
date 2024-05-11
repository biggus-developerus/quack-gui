__all__ = ("ElementHelper",)

from abc import ABC
from typing import Union

from quack.element import Element
from quack.elements import Image, InputBox, Rect, Text
from quack.font import FontManager


class ElementHelper(
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
        rect = Rect(pos, *w_and_h, colour=colour, border_width=border_width, border_radius=border_radius)
        self.add_element(rect)
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
        text_element = Text(text, size, font, pos, colour=colour)

        self.add_element(text_element)

        return text_element

    def add_inputbox(
        self,
        size: tuple[int, int],
        pos: tuple[int, int] = (0, 0),
        *,
        colour: tuple[int, int, int] = (255, 255, 255),
        border_width: int = 0,
        border_radius: int = 0,
    ) -> InputBox:
        inputbox = InputBox(
            size,
            pos,
            colour=colour,
            border_width=border_width,
            border_radius=border_radius,
        )

        self.add_element(inputbox)

        return inputbox

    def add_image(self, path_or_data: Union[str, bytes], pos: tuple[int, int] = (0, 0)) -> Image:
        image = Image(path_or_data, pos)
        self.add_element(image)
        return image
