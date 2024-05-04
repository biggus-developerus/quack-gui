__all__ = ("Element",)

import asyncio
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Callable, Coroutine, Optional

import pygame

if TYPE_CHECKING:
    from quack.dispatcher import EventContext

ElementCB = Callable[["EventContext"], Coroutine[None, None, None]]


class Element(ABC):
    def __init__(self, pos: tuple[int, int]) -> None:
        self._on_click_cb: Optional[ElementCB] = None
        self._on_hover_cb: Optional[ElementCB] = None
        self._on_hover_exit_cb: Optional[ElementCB] = None

        self.pos: tuple[int, int] = pos
        self.is_hovered: bool = False

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
        loop.create_task(self._on_click_cb(event_context))

    def dispatch_hover(self, loop: asyncio.AbstractEventLoop, event_context: "EventContext") -> None:
        loop.create_task(self._on_hover_cb(event_context))

    def dispatch_hover_exit(self, loop: asyncio.AbstractEventLoop, event_context: "EventContext") -> None:
        loop.create_task(self._on_hover_exit_cb(event_context))
