from typing import TYPE_CHECKING

import pygame

from quack.dispatcher import EventContext

if TYPE_CHECKING:
    from quack.app import App


async def on_quit(app: "App", _: pygame.event.Event) -> None:
    app.stop()


async def on_mouse_button_up(app: "App", event: pygame.event.Event) -> None:
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
                element.dispatch_click(app._loop, event_ctx)

            break  # what if some retard wants 2 elements in the same place and also wants to trigeger the event for both???? SOB X50 KYS!?


async def on_mouse_move(app: "App", event: pygame.event.Event) -> None:
    pos = event.pos
    left, middle, right = event.buttons  # TODO: moving elements??!?!?

    event_ctx = EventContext(app)
    event_ctx.mouse_pos = pos

    for element in app.get_elements():
        collides = element.get_rect().collidepoint((pos))

        if not collides and element.is_hovered:
            element.is_hovered = False

            if element._on_hover_exit_cb:
                event_ctx.element = element
                event_ctx.mouse_pos = pos

                element.dispatch_hover_exit(app._loop, event_ctx)

            continue

        if collides:
            event_ctx.element = element
            element.is_hovered = True

            if element._on_hover_cb:
                element.dispatch_hover(app._loop, event_ctx)
                return
