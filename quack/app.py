__all__ = ("App",)

from typing import Callable, Any, Coroutine, Optional

import asyncio
import time
import pygame

from quack.abc import Drawable
from quack.font import FontManager, Text
from quack.rect import Rect


class App:
    def __init__(self, w: int, h: int, *, caption: str = "Quack App", display_flags: int = pygame.SHOWN, tick: int = 60) -> None:
        pygame.display.set_caption(caption)

        self._screen = pygame.display.set_mode((w, h), flags=display_flags)

        self._asyncio_queue: asyncio.Queue = asyncio.Queue()
        self._loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
        self._running: bool = False

        self.tick: int = tick

        self._background_colour: tuple[int, int, int] = (0, 0, 0)

        self._drawables: list[Drawable] = []
        self._pre_draw_cb: Optional[Callable[..., Coroutine[Any, Any, Any]]] = None

        self._frames_per_sec: int = 0

    def set_background_colour(self, r: int, g: int, b: int) -> None:
        self._background_colour = (r, g, b)

    def add_inputbox(
        self,
        w_and_h: tuple[int, int],
        position: tuple[int, int],
        *,
        colour: tuple[int, int, int] = (255, 255, 255),
        border_width: int = 3,
        border_radius=50,
    ) -> Rect:
        self._drawables.append(
            rect := Rect(*position, *w_and_h, colour=colour, border_width=border_width, border_radius=border_radius)
        )
        return rect

    def add_text(
        self,
        text: str,
        size: int,
        pos: tuple[int, int],
        *,
        font: str = FontManager.get_default_font(),
        colour: tuple[int, int, int] = (255, 255, 255),
    ) -> Text:
        self._drawables.append(text := Text(text, size, font, pos, colour=colour))
        return text

    def add_pre_draw_cb(self, cb: Callable[..., Coroutine[Any, Any, Any]]) -> None:
        if not asyncio.iscoroutinefunction(cb):
            raise ValueError("Pre draw callback must be an async func!")
        
        self._pre_draw_cb = cb

    def get_fps(self) -> int:
        return self._frames_per_sec

    def _pygame_event_loop(self) -> None:
        while True:
            event = pygame.event.wait()
            asyncio.run_coroutine_threadsafe(self._asyncio_queue.put(event), self._loop)

    async def _draw_loop(self) -> None:
        last_tick = time.time()
        frames = 0
    
        while self._running:
            self._screen.fill(self._background_colour)

            if self._pre_draw_cb:
                await self._pre_draw_cb(self)

            for drawable in self._drawables:
                drawable.draw(self._screen)

            pygame.display.flip()

            frames += 1

            if (elapsed:=(ctime:=time.time()) - last_tick) >= 1.0:
                self._frames_per_sec = frames / elapsed
                
                frames = 0
                last_tick = ctime

            await asyncio.sleep(1 / self.tick)

    async def _handle_events(self) -> None:
        while self._running:
            event: pygame.event.Event = await self._asyncio_queue.get()

            if event.type == pygame.QUIT:
                self.stop()

        self.stop()

    def run(self) -> None:
        self._running = True

        t1 = self._loop.run_in_executor(None, self._pygame_event_loop)
        t2 = self._loop.create_task(self._handle_events())
        t3 = self._loop.create_task(self._draw_loop())

        self._loop.run_forever()

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
