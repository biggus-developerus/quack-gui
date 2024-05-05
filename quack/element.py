__all__ = (
    "Element",
    "ElementTaskType",
)

import asyncio
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Coroutine, Optional

import pygame
from aenum import Enum

from quack.animation import Animation, AnimationType

if TYPE_CHECKING:
    from quack.dispatcher import EventContext

ElementCB = Callable[["EventContext"], Coroutine[None, None, None]]


class ElementTaskType(Enum):
    ON_CLICK = 0
    ON_CLICK_UP = 1

    ON_HOVER = 2
    ON_HOVER_EXIT = 3


ELEMENT_TASK_TYPE_TO_PYGAME_EVENT: dict[ElementTaskType, int] = {
    ElementTaskType.ON_CLICK: pygame.MOUSEBUTTONDOWN,
    ElementTaskType.ON_CLICK_UP: pygame.MOUSEBUTTONUP,
    ElementTaskType.ON_HOVER: pygame.MOUSEMOTION,
    ElementTaskType.ON_HOVER_EXIT: pygame.MOUSEMOTION,
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

        self._tasks: dict[ElementTaskType, Optional[asyncio.Task]] = {
            ElementTaskType.ON_CLICK: None,
            ElementTaskType.ON_CLICK_UP: None,
            ElementTaskType.ON_HOVER: None,
            ElementTaskType.ON_HOVER_EXIT: None,
        }

        self._callbacks: dict[ElementTaskType, Optional[ElementCB]] = {
            ElementTaskType.ON_CLICK: None,
            ElementTaskType.ON_CLICK_UP: None,
            ElementTaskType.ON_HOVER: None,
            ElementTaskType.ON_HOVER_EXIT: None,
        }

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None: ...

    @abstractmethod
    def get_rect(self) -> pygame.Rect: ...

    @abstractmethod
    def get_size(self) -> tuple[int, int]: ...

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

    def call_cb(self, loop: asyncio.AbstractEventLoop, cb_type: ElementTaskType, event_context: "EventContext") -> None:
        if not (cb := self._callbacks.get(cb_type, None)):
            return

        task = self._tasks.get(cb_type, None)

        if task and not task.done() and not task.cancelled():
            return

        self._tasks[cb_type] = loop.create_task(cb(event_context))

    def on_click(self, cb: ElementCB) -> None:
        self.set_cb(ElementTaskType.ON_CLICK, cb)

    def on_click_up(self, cb: ElementCB) -> None:
        self.set_cb(ElementTaskType.ON_CLICK_UP, cb)

    def on_hover(self, cb: ElementCB) -> None:
        self.set_cb(ElementTaskType.ON_HOVER, cb)

    def on_hover_exit(self, cb: ElementCB) -> None:
        self.set_cb(ElementTaskType.ON_HOVER_EXIT, cb)
