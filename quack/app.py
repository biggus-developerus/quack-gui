__all__ = ("App",)

import asyncio
import time
from typing import Optional

import pygame

import quack.internal_events as internal_events
from quack.dispatcher import Dispatcher
from quack.element_manager import ElementManager
from quack.font import FontManager


class App(ElementManager):
    def __init__(
        self,
        w: int,
        h: int,
        *,
        caption: str = "Quack App",
        display_flags: int = pygame.SHOWN,
        tick: int = 60,
    ) -> None:
        super().__init__()

        pygame.init()

        self._screen: Optional[pygame.Surface] = None

        self._size: tuple[int, int] = (w, h)
        self._caption: str = caption
        self._display_flags: int = display_flags

        self._asyncio_queue: asyncio.Queue = asyncio.Queue()
        self._loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self._running: bool = False

        self.tick: int = tick
        self.frames_per_sec: int = 0

        self.background_colour: tuple[int, int, int] = (0, 0, 0)

    def set_background_colour(self, r: int, g: int, b: int) -> None:
        self._background_colour = (r, g, b)

    def get_fps(self) -> int:
        return self.frames_per_sec

    def _pygame_event_loop(self) -> None:
        while True:
            event = pygame.event.wait()
            asyncio.run_coroutine_threadsafe(self._asyncio_queue.put(event), self._loop)

    async def _handle_events(self) -> None:
        while self._running:
            event = await self._asyncio_queue.get()
            Dispatcher.dispatch(self._loop, event.type, self, event)

        self.stop()

    async def _draw_loop(self) -> None:
        last_tick = time.time()
        ticks = 0

        while self._running:
            self._screen.fill(self._background_colour)

            for element in self.get_elements():
                element.draw(self._screen)

            pygame.display.flip()

            ticks += 1

            if (elapsed := (ctime := time.time()) - last_tick) >= 1.0:
                self.frames_per_sec = ticks / elapsed

                ticks = 0
                last_tick = ctime

            await asyncio.sleep(1 / self.tick)

    def _init_internal_events(self) -> None:
        Dispatcher.add_event(pygame.QUIT, internal_events.on_quit)
        Dispatcher.add_event(pygame.MOUSEBUTTONUP, internal_events.on_mouse_button_up)
        Dispatcher.add_event(pygame.MOUSEBUTTONDOWN, internal_events.on_mouse_button_down)
        Dispatcher.add_event(pygame.MOUSEMOTION, internal_events.on_mouse_move)

        Dispatcher.add_event(pygame.WINDOWLEAVE, internal_events.on_window_leave)

    def run(self) -> None:
        self._init_internal_events()
        self._running = True

        FontManager.init()
        pygame.display.set_caption(self._caption)

        self._screen = pygame.display.set_mode(self._size, flags=self._display_flags)

        t1 = self._loop.run_in_executor(None, self._pygame_event_loop)
        t2 = self._loop.create_task(self._handle_events())
        t3 = self._loop.create_task(self._draw_loop())

        try:
            self._loop.run_forever()
        except KeyboardInterrupt:
            pass
        finally:
            t1.cancel()
            t2.cancel()
            t3.cancel()

            pygame.quit()

    def stop(self) -> None:
        self._running = False
        self._loop.stop()


if __name__ == "__main__":
    app = App(800, 600)
    app.run()
