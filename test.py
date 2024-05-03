import pygame

import quack

quack.init()

app = quack.App(500, 500, tick=60)
app.set_background_colour(20, 20, 20)

t = app.add_text(
    "title_text",
    "**_KEEWL PROXY_**",
    30,
    (175, 10),
)

app.add_text("fps_text", "**FPS - {}**", 40, (0, 0))
app.add_inputbox("name_inp", (300, 30), (100, 250), border_width=1, border_radius=1)


async def quit(*args, **kwargs):
    app.stop()


quack.Dispatcher.add_event(pygame.QUIT, quit)

app.run()
