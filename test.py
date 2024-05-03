import random

import quack

quack.init()

app = quack.App(500, 500, tick=60)
app.set_background_colour(20, 20, 20)

app.add_inputbox("name_inp", (300, 30), (100, 250), border_width=1, border_radius=1)

title_text = app.add_text(
    "title_text",
    "**_KEEWL PROXY_**",
    30,
    (175, 10),
)

fps_text = app.add_text("fps_text", "**FPS - {}**", 40, (0, 0))


@title_text.on_click
async def title_text_click(ctx: quack.EventContext) -> None:
    ctx.element.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


@fps_text.on_click
async def fps_text_click(ctx: quack.EventContext) -> None:
    ctx.element.colour = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    ctx.element.text = "**FPS - {}**".format(int(app.get_fps()))


@fps_text.on_hover
async def fps_text_hover(ctx: quack.EventContext) -> None:
    ctx.element.colour = (30, 30, 30)


app.run()
