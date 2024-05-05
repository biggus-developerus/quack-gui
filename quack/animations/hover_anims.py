__all__ = (
    "hover_dim",
    "unhover_dim",
)

from quack.dispatcher import EventContext

async def hover_dim(ctx: EventContext) -> None:
    if not getattr(ctx.element, "original_colour", None):
        ctx.element.original_colour = ctx.element.colour
        
    ctx.element.colour = (100, 100, 100)

async def unhover_dim(ctx: EventContext) -> None:  
    ctx.element.colour = ctx.element.original_colour