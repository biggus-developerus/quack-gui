import time

import quack

app = quack.App((700, 700), tick=165)
app.set_background_colour(20, 20, 20)

app.clicks = 0
app.last_click = time.time()

click_text = app.add_text("**CLICK!** ", 100, (0, 0), colour=(255, 255, 0))

click_text.apply_animation(quack.AnimationType.HOVER_DIM, 0.01)
click_text.center()


cps_text = app.add_text("__YOUR CPS IS: 0__", 50, (0, 0), colour=(0, 255, 0))
cps_text.center_x()

cps_box = app.add_rect(app.get_size(), (0, 0), colour=(0, 0, 0), border_width=-1)


@cps_box.on_click
async def on_click(ctx: quack.EventContext) -> None:
    ctx.app.clicks += 1

    click_text.text = f"**CLICK! {ctx.app.clicks}**"
    click_text.center()


app.run()
