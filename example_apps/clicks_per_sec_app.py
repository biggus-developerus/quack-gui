import quack
import time

app = quack.App(500, 500, tick=500)
app.set_background_colour(20, 20, 20)

title_text = app.add_text("**CLICK ME!**", 50, (0, 0), colour=(255, 255, 0))
title_text.apply_animation(quack.AnimationType.HOVER_DIM, title_text)
title_text.pos = (500 - title_text.get_rect().width) // 2, 250

cps_text = app.add_text("__YOUR CPS IS: 0__", 50, (0, 0), colour=(0, 255, 0))
cps_text.pos = (500 - cps_text.get_rect().width) // 2, 0

print(cps_text.get_size())

clicks = 0
last_click: float = time.time()

@title_text.on_click
async def on_click(ctx: quack.EventContext) -> None:
    global clicks, last_click

    ctx.element.text = f"**CLICK ME! {clicks}**"

    if time.time() - last_click >= 1:
        cps_text.text = f"__YOUR CPS IS: {clicks}__"

        clicks = 0
        last_click = time.time()

        return
    
    clicks += 1

app.run()
