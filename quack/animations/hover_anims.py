__all__ = (
    "hover_dim",
    "unhover_dim",
)

from typing import Optional

from quack.dispatcher import EventContext


async def hover_dim(ctx: EventContext, anim_duration: Optional[float] = None) -> None:
    ctx.element.colour = tuple(int(value * 0.5) for value in ctx.element.original_colour)


async def unhover_dim(ctx: EventContext, anim_duration: Optional[float] = None) -> None:
    ctx.element.colour = ctx.element.original_colour
