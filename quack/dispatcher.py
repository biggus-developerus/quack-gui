__all__ = (
    "Dispatcher",
    "Event",
    "EventContext",
)

import asyncio
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, Coroutine, Optional

if TYPE_CHECKING:
    from quack.app import App
    from quack.element import Element

T = Callable[..., Coroutine[Any, Any, Any]]


class Event:
    def __init__(self, cb: T, done_cb: Optional[Callable] = None) -> None:
        self.cb: T = cb
        self.done_cb: Optional[Callable] = done_cb


@dataclass
class EventContext:
    app: Optional["App"] = None
    element: Optional["Element"] = None
    mouse_pos: Optional[tuple[int, int]] = None
    key: Optional[int] = None
    key_unicode: Optional[str] = None


class Dispatcher:
    _events: dict[int, Event] = {}

    @classmethod
    def add_event(cls, event_type: int, event_cb: T, done_cb: Optional[Callable] = None) -> None:
        if not asyncio.iscoroutinefunction(event_cb):
            raise ValueError("Event callback must be a coroutine function")

        cls._events[event_type] = Event(event_cb, done_cb)

    @classmethod
    def dispatch(
        cls,
        loop: asyncio.AbstractEventLoop,
        event_type: int,
        *args,
        **kwargs,
    ) -> None:
        event = cls._events.get(event_type, None)

        if not event:
            return

        t = loop.create_task(event.cb(*args, **kwargs))

        if event.done_cb:
            t.add_done_callback(event.done_cb)
