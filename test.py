import asyncio

import quack

quack.init()

app = quack.App(500, 500, tick=500)
app.set_background_colour(20, 20, 20)

app.add_inputbox("name_inp", (300, 30), (100, 250), border_width=1, border_radius=1)

title_text = app.add_text(
    "title_text",
    "**PROXY**",
    50,
    ((app._screen.get_size()[0] - 144) // 2, 10),
)

fps_text = app.add_text("fps_text", "**FPS**", 40, (0, 0))


@title_text.on_hover
async def title_text_hover(ctx: quack.EventContext) -> None:
    if ctx.element.colour[0] == 100:
        ctx.element.colour = (100, 100, 100)
        return
    
    for i in range(ctx.element.colour[0], 100, -1):
        ctx.element.colour = (i, i, i)
        await asyncio.sleep(0.001)


@title_text.on_hover_exit
async def title_text_hover_exit(ctx: quack.EventContext) -> None:
    if ctx.element.colour[0] == 255:
        ctx.element.colour (255, 255, 255)
        return
    
    for i in range(ctx.element.colour[0], 256):
        ctx.element.colour = (i, i, i)
        await asyncio.sleep(0.001)


app.run()
