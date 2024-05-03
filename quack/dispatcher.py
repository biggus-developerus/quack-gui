__all__ = (
    "Dispatcher",
    "Event",
)

import asyncio
from typing import Any, Callable, Coroutine, Optional

T = Callable[..., Coroutine[Any, Any, Any]]


class Event:
    def __init__(self, cb: T, done_cb: Optional[Callable] = None) -> None:
        self.cb: T = cb
        self.done_cb: Optional[Callable] = done_cb


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
