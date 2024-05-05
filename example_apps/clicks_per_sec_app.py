import time

import quack

app = quack.App((700, 700), tick=165)
app.set_background_colour(20, 20, 20)

cps_box = app.add_rect(app.get_size(), (0, 0), colour=(0, 0, 0), border_width=-1)

click_text = app.add_text("**CLICK!**", 100, (0, 0), colour=(255, 255, 0))
click_text.pos = (app.get_width() - click_text.get_rect().width) // 2, app.get_height() // 2
click_text.apply_animation(quack.AnimationType.HOVER_DIM, 0.01)

cps_text = app.add_text("__YOUR CPS IS: 0__", 50, (0, 0), colour=(0, 255, 0))
cps_text.pos = (app.get_width() - cps_text.get_rect().width) // 2, 0

fps_text = app.add_text("__YOUR FPS IS: 0__", 30, (0, 0), colour=(0, 0, 255))
fps_text.pos = (app.get_width() - fps_text.get_rect().width), 0

counter_text = app.add_text("TIME: 0", 30, (0, 0), colour=(255, 0, 0))

clicks = 0
last_click: float = time.time()


@counter_text.on_tick
async def timer(ctx: quack.EventContext) -> None:
    global last_click, clicks

    if clicks == 0:
        last_click = time.time()
        clicks = 0

        click_text.text = f"**CLICK! {clicks}**"
        click_text.pos = (app.get_width() - click_text.get_rect().width) // 2, app.get_height() // 2

        return

    if time.time() - last_click >= 1:
        cps_text.text = f"__YOUR CPS IS: {clicks}__"
        last_click = time.time()
        clicks = 0

    ctx.element.text = f"TIME: {time.time() - last_click:.1f}"


@fps_text.on_tick
async def fps_set(ctx: quack.EventContext) -> None:
    ctx.element.text = f"__YOUR FPS IS: {int(ctx.app.get_fps())}__"
    ctx.element.pos = (app.get_width() - ctx.element.get_rect().width), 0


@cps_box.on_click
async def on_click(_: quack.EventContext) -> None:
    global clicks

    clicks += 1

    click_text.text = f"**CLICK! {clicks}**"
    click_text.pos = (app.get_width() - click_text.get_rect().width) // 2, app.get_height() // 2


app.run()
