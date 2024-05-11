from typing import TYPE_CHECKING

import pygame

from quack.dispatcher import EventContext
from quack.element import ElementTaskType

if TYPE_CHECKING:
    from quack.app import App

# TODO: Address the issue of calling the CBs of two different elements when they overshadow each other

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

            if left:
                element.is_clicked = False
                await element.call_cb(app._loop, ElementTaskType.ON_CLICK_UP, event_ctx)


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
            
            if left:
                element.is_clicked = True
                element.is_activated = True
                await element.call_cb(app._loop, ElementTaskType.ON_CLICK, event_ctx)
        else:
            if element.is_activated and left:
                element.is_activated = False # TODO: Cb for this ig?


async def on_mouse_move(app: "App", event: pygame.event.Event) -> None:
    pos = event.pos
    left, middle, right = event.buttons  # TODO: moving elements??!?!?

    event_ctx = EventContext(app)
    event_ctx.mouse_pos = pos

    for element in app.get_elements():
        collides = element.get_rect().collidepoint((pos))

        if not collides and element.is_hovered or element.is_clicked:
            if element.is_hovered:
                element.is_hovered = False

                event_ctx.element = element
                await element.call_cb(app._loop, ElementTaskType.ON_HOVER_EXIT, event_ctx)

            if element.is_clicked:
                element.is_clicked = False

                event_ctx.element = element
                await element.call_cb(app._loop, ElementTaskType.ON_CLICK_UP, event_ctx)

            continue

        if collides:
            if element.is_hovered:
                continue

            event_ctx.element = element
            element.is_hovered = True

            await element.call_cb(app._loop, ElementTaskType.ON_HOVER, event_ctx)

async def on_key_down(app: "App", event: pygame.event.Event) -> None:
    unicode, key, mod = event.unicode, event.key, event.mod

    event_ctx = EventContext(app)
    event_ctx.key_pressed = unicode

    for element in app.get_elements():
        if element.is_activated:
            event_ctx.element = element
            await element.call_cb(app._loop, ElementTaskType.ON_KEY, event_ctx)

async def on_key_up(app: "App", event: pygame.event.Event) -> None:
    unicode, key, mod = event.unicode, event.key, event.mod

    event_ctx = EventContext(app)
    event_ctx.key_pressed = unicode

    for element in app.get_elements():
        if element.is_activated:
            event_ctx.element = element
            await element.call_cb(app._loop, ElementTaskType.ON_KEY_UP, event_ctx)

async def on_window_leave(app: "App", event: pygame.event.Event) -> None: ...
