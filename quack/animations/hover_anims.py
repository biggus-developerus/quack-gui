__all__ = (
    "hover_dim",
    "unhover_dim",
)

from quack.dispatcher import EventContext

async def hover_dim(ctx: EventContext, dimming_factor: float = 0.5) -> None:
    subtract_20 = lambda number: number - 20 if number-20 > -1 else 0 

    ctx.element.colour = subtract_20(ctx.element.colour[0]), subtract_20(ctx.element.colour[1]), subtract_20(ctx.element.colour[2])

async def unhover_dim(ctx: EventContext) -> None:
    ...
