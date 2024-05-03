from typing import TYPE_CHECKING

import pygame

from quack.dispatcher import EventContext

if TYPE_CHECKING:
    from quack.app import App


async def on_quit(app: "App", _: pygame.event.Event) -> None:
    app.stop()


async def on_mouse_button_down(app: "App", event: pygame.event.Event) -> None:
    pos = event.pos

    left = event.button == pygame.BUTTON_LEFT
    right = event.button == pygame.BUTTON_RIGHT
    middle = event.button == pygame.BUTTON_MIDDLE

    wheel_up = event.button == pygame.BUTTON_WHEELUP
    wheel_down = event.button == pygame.BUTTON_WHEELDOWN

    event_ctx = EventContext(app)

    for element in app.get_elements():
        if element.get_rect().collidepoint((pos)):
            event_ctx.element = element
            event_ctx.mouse_pos = pos

            if left and element._on_click_cb:
                app._loop.create_task(element._on_click_cb(event_ctx))
                return
