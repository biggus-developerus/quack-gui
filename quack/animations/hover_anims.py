__all__ = (
    "hover_dim",
    "unhover_dim",
)

import asyncio

from quack.dispatcher import EventContext


async def hover_dim(ctx: EventContext) -> None:
    dimmed = tuple(int(value * 0.5) for value in ctx.element.original_colour)
    colour = ctx.element.original_colour

    if ctx.element.animation_duration:
        sleep_time = ctx.element.animation_duration / (ctx.app.get_fps() if ctx.app.get_fps() > 0 else 60)

        max_difference = max(abs(colour[i] - dimmed[i]) for i in range(3))

        step_sizes = [(dimmed[i] - colour[i]) / max_difference for i in range(3)]

        for i in range(max_difference):
            r = max(0, min(255, int(colour[0] + i * step_sizes[0])))
            g = max(0, min(255, int(colour[1] + i * step_sizes[1])))
            b = max(0, min(255, int(colour[2] + i * step_sizes[2])))

            ctx.element.colour = (r, g, b)
            await asyncio.sleep(sleep_time)
    else:
        ctx.element.colour = dimmed


async def unhover_dim(ctx: EventContext) -> None:
    original_colour = ctx.element.original_colour
    colour = ctx.element.colour

    if ctx.element.animation_duration:
        sleep_time = ctx.element.animation_duration / 60

        max_difference = max(abs(colour[i] - original_colour[i]) for i in range(3))

        if max_difference != 0: # prevent div by zero
            step_sizes = [(original_colour[i] - colour[i]) / max_difference for i in range(3)]

            for i in range(max_difference):
                r = max(0, min(255, int(colour[0] + i * step_sizes[0])))
                g = max(0, min(255, int(colour[1] + i * step_sizes[1])))
                b = max(0, min(255, int(colour[2] + i * step_sizes[2])))

                ctx.element.colour = (r, g, b)
                await asyncio.sleep(sleep_time)
    else:
        ctx.element.colour = original_colour
