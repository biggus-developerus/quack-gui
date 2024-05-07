__all__ = (
    "Element",
    "ElementTaskType",
    "ElementPosType",
)

import asyncio
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Coroutine, Optional, Protocol, Union

import pygame
from aenum import Enum

from quack.animation import Animation, AnimationType

if TYPE_CHECKING:
    from quack.app import App
    from quack.dispatcher import EventContext

ElementCB = Callable[["EventContext"], Coroutine[None, None, None]]


class HasGetRect(Protocol):
    def get_rect(self) -> pygame.Rect: ...


class ElementTaskType(Enum):
    ON_CLICK = 0
    ON_CLICK_UP = 1

    ON_HOVER = 2
    ON_HOVER_EXIT = 3

    ON_TICK = 4


class ElementPosType(Enum):
    CENTER = 0

    TOP = 1
    BOTTOM = 2

    MOST_LEFT = 3
    MOST_RIGHT = 4


ELEMENT_TASK_TYPE_TO_PYGAME_EVENT: dict[ElementTaskType, int] = {
    ElementTaskType.ON_CLICK: pygame.MOUSEBUTTONDOWN,
    ElementTaskType.ON_CLICK_UP: pygame.MOUSEBUTTONUP,
    ElementTaskType.ON_HOVER: pygame.MOUSEMOTION,
    ElementTaskType.ON_HOVER_EXIT: pygame.MOUSEMOTION,
    ElementTaskType.ON_TICK: -1,
}

ELEMENT_TASK_OPPOSITE: dict[ElementTaskType, ElementTaskType] = {
    ElementTaskType.ON_HOVER: ElementTaskType.ON_HOVER_EXIT,
    ElementTaskType.ON_HOVER_EXIT: ElementTaskType.ON_HOVER,
}


class ElementMixin(ABC):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Element(ElementMixin, Animation):
    def __init__(self, pos: tuple[int, int], colour: tuple[int, int, int] = (255, 255, 255)) -> None:
        Animation.__init__(self, animation_type=AnimationType.NONE)

        self.pos: tuple[int, int] = pos

        self.colour: tuple[int, int, int] = colour
        self.original_colour: tuple[int, int, int] = colour

        self.is_hovered: bool = False
        self.is_clicked: bool = False

        self._app: Optional["App"] = None

        # TODO: Loop through the enum ElementTaskType and set the values of the dicts below accordingly instead.

        self._tasks: dict[ElementTaskType, Optional[asyncio.Task]] = {
            ElementTaskType.ON_CLICK: None,
            ElementTaskType.ON_CLICK_UP: None,
            ElementTaskType.ON_HOVER: None,
            ElementTaskType.ON_HOVER_EXIT: None,
            ElementTaskType.ON_TICK: None,
        }

        self._callbacks: dict[ElementTaskType, Optional[ElementCB]] = {
            ElementTaskType.ON_CLICK: None,
            ElementTaskType.ON_CLICK_UP: None,
            ElementTaskType.ON_HOVER: None,
            ElementTaskType.ON_HOVER_EXIT: None,
            ElementTaskType.ON_TICK: None,
        }

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None: ...

    @abstractmethod
    def get_rect(self) -> pygame.Rect: ...

    def get_size(self) -> tuple[int, int]:
        rect = self.get_rect()
        return (rect.width, rect.height)

    def get_width(self) -> int:
        return self.get_size()[0]

    def get_height(self) -> int:
        return self.get_size()[1]

    def set_app(self, app: "App") -> None:
        self._app = app

    def fancy_set_x_pos(self, x: ElementPosType, surface: Optional[HasGetRect] = None) -> None:
        if x == ElementPosType.CENTER:
            self.center_x(surface)
        elif x == ElementPosType.MOST_LEFT:
            self.set_pos(x=0)
        elif x == ElementPosType.MOST_RIGHT:
            if not self._app:
                raise ValueError(
                    f"This element {self.__class__} does not have its _app attr set. Make sure you added this element via the ElementManager (app.add_rect, app.add_element, etc.)"
                )

            self.set_pos(x=self._app.get_width() - self.get_width())

    def fancy_set_y_pos(self, y: ElementPosType, surface: Optional[HasGetRect] = None) -> None: 
        if y == ElementPosType.CENTER:
            self.center_y(surface)
        elif y == ElementPosType.TOP:
            self.set_pos(y=0)
        elif y == ElementPosType.BOTTOM:
            self.set_pos(y=self._app.get_height() - self.get_height())

    def set_pos(self, x: Union[int, None] = None, y: Union[int, None] = None, surface: Optional[HasGetRect] = None) -> None:
        if x is not None:
            self.pos = (x, self.pos[1]) if isinstance(x, int) else self.fancy_set_x_pos(x, surface)

        if y is not None:
            self.pos = (self.pos[0], y) if isinstance(y, int) else self.fancy_set_y_pos(y, surface)

    def center(self, surface: Optional[HasGetRect] = None) -> None:
        self.center_x(surface)
        self.center_y(surface)

    def center_x(self, surface: Optional[HasGetRect] = None) -> None:
        if not self._app and not surface:
            raise ValueError(
                f"This element {self.__class__} does not have its _app attr set. Make sure you added this element via the ElementManager (app.add_rect, app.add_element, etc.)"
            )

        if surface:
            x = surface.get_rect().x + (surface.get_width() - self.get_width()) // 2
        else:
            x = (self._app._screen.get_rect().width - self.get_width()) // 2

        self.set_pos(x=x)

    def center_y(self, surface: Optional[HasGetRect] = None) -> None:
        if not self._app and not surface:
            raise ValueError(
                f"This element {self.__class__} does not have its _app attr set. Make sure you added this element via the ElementManager (app.add_rect, app.add_element, etc.)"
            )

        if surface:
            y = surface.get_rect().y + (surface.get_height() - self.get_height()) // 2
        else:
            y = (self._app._screen.get_rect().height - self.get_height()) // 2

        self.set_pos(y=y)

    def change_colour(self, rgb: tuple[int, int, int]) -> None:
        self.colour = rgb
        self.original_colour = rgb

    def set_animation(self, animation: Animation) -> None:
        self._animation = animation

    def get_cb(self, cb_type: ElementTaskType) -> Optional[ElementCB]:
        return self._callbacks.get(cb_type, None)

    def set_cb(self, cb_type: ElementTaskType, cb: ElementCB) -> None:
        if not asyncio.iscoroutinefunction(cb):
            raise ValueError(f"Element event type {cb_type} callback must be a coroutine function")

        if self.animation_type.value[-1] == ELEMENT_TASK_TYPE_TO_PYGAME_EVENT[cb_type]:
            raise ValueError(
                f"Callback type conflict: a callback is already set for an element animation ({self.animation_type.name})"
            )

        self._callbacks[cb_type] = cb

    async def call_cb(
        self,
        loop: asyncio.AbstractEventLoop,
        cb_type: ElementTaskType,
        event_context: "EventContext",
    ) -> None:
        if not (cb := self._callbacks.get(cb_type, None)):
            return

        task = self._tasks.get(cb_type, None)
        opp_task = self._tasks.get(ELEMENT_TASK_OPPOSITE.get(cb_type, None), None)

        if opp_task:
            opp_task.cancel()

            try:
                await opp_task
            except asyncio.CancelledError:
                pass

        if task:
            task.cancel()

            try:
                await task
            except asyncio.CancelledError:
                pass

        self._tasks[cb_type] = loop.create_task(cb(event_context))

    def on_click(self, cb: ElementCB) -> None:
        self.set_cb(ElementTaskType.ON_CLICK, cb)

    def on_click_up(self, cb: ElementCB) -> None:
        self.set_cb(ElementTaskType.ON_CLICK_UP, cb)

    def on_hover(self, cb: ElementCB) -> None:
        self.set_cb(ElementTaskType.ON_HOVER, cb)

    def on_hover_exit(self, cb: ElementCB) -> None:
        self.set_cb(ElementTaskType.ON_HOVER_EXIT, cb)

    def on_tick(self, cb: ElementCB) -> None:
        self.set_cb(ElementTaskType.ON_TICK, cb)
