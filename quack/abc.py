__all__ = ("Element",)

import asyncio
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Coroutine, Optional

import pygame
from aenum import Enum

if TYPE_CHECKING:
    from quack.dispatcher import EventContext

ElementCB = Callable[["EventContext"], Coroutine[None, None, None]]


class ElementTaskType(Enum):
    ON_CLICK = 0
    ON_HOVER = 1
    ON_HOVER_EXIT = 2
    ON_TICK = 3  # soon


class Element(ABC):
    def __init__(self, pos: tuple[int, int]) -> None:
        self._on_click_cb: Optional[ElementCB] = None
        self._on_hover_cb: Optional[ElementCB] = None
        self._on_hover_exit_cb: Optional[ElementCB] = None

        self.pos: tuple[int, int] = pos
        self.is_hovered: bool = False

        self._tasks: dict[ElementTaskType, Optional[asyncio.Task]] = {
            ElementTaskType.ON_CLICK: None,
            ElementTaskType.ON_HOVER: None,
            ElementTaskType.ON_HOVER_EXIT: None,
            ElementTaskType.ON_TICK: None,  # soon
        }

    @abstractmethod
    def draw(self, surface: pygame.Surface) -> None: ...

    @abstractmethod
    def get_rect(self) -> pygame.Rect: ...

    @abstractmethod
    def get_size(self) -> tuple[int, int]: ...

    def on_click(self, cb: ElementCB) -> None:
        if not asyncio.iscoroutinefunction(cb):
            raise ValueError("Element on click callback must be a coroutine function")

        self._on_click_cb = cb

    def on_hover(self, cb: ElementCB) -> None:
        if not asyncio.iscoroutinefunction(cb):
            raise ValueError("Element on hover callback must be a coroutine function")

        self._on_hover_cb = cb

    def on_hover_exit(self, cb: ElementCB) -> None:
        if not asyncio.iscoroutinefunction(cb):
            raise ValueError("Element on hover exit callback must be a coroutine function")

        self._on_hover_exit_cb = cb

    def dispatch_click(self, loop: asyncio.AbstractEventLoop, event_context: "EventContext") -> None:
        task = self._tasks[ElementTaskType.ON_CLICK]

        if task:
            if not task.done() and not task.cancelled() and not task.cancelling() > 0:
                print("ongoing click task...")
                return

        self._tasks[ElementTaskType.ON_CLICK] = loop.create_task(self._on_click_cb(event_context))

    def dispatch_hover(self, loop: asyncio.AbstractEventLoop, event_context: "EventContext") -> None:
        task = self._tasks[ElementTaskType.ON_HOVER]

        if task:
            if not task.done() and not task.cancelled() and not task.cancelling() > 0:
                print("ongoing hover task...")
                return

        self._tasks[ElementTaskType.ON_HOVER] = loop.create_task(self._on_hover_cb(event_context))

    def dispatch_hover_exit(self, loop: asyncio.AbstractEventLoop, event_context: "EventContext") -> None:
        task = self._tasks[ElementTaskType.ON_HOVER_EXIT]

        if task:
            if not task.done() and not task.cancelled() and not task.cancelling() > 0:
                print("ongoing hover exit task...")
                return

        self._tasks[ElementTaskType.ON_HOVER_EXIT] = loop.create_task(self._on_hover_exit_cb(event_context))
