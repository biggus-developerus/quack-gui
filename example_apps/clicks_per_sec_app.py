import quack
import time

app = quack.App(500, 500)
app.set_background_colour(20, 20, 20)

click_me = app.add_text("**CLICK ME!**", 100, (0, 0), colour=(255, 255, 0))
click_me.apply_animation(quack.AnimationType.HOVER_DIM)
click_me.pos = (500 - click_me.get_rect().width) // 2, 250

cps_text = app.add_text("__YOUR CPS IS: 0__", 50, (0, 0), colour=(0, 255, 0))
cps_text.pos = (500 - cps_text.get_rect().width) // 2, 0

counter_text = app.add_text("TIME: 0", 30, (0, 0), colour=(255, 0, 0))
counter_text.apply_animation(quack.AnimationType.HOVER_DIM)

clicks = 0
last_click: float = time.time()

@counter_text.on_tick
async def timer(ctx: quack.EventContext) -> None:
    global last_click, clicks

    if clicks == 0:
        last_click = time.time()
        clicks = 0

        click_me.text = f"**CLICK ME! {clicks}**"

        return

    if time.time() - last_click >= 1:
        cps_text.text = f"__YOUR CPS IS: {clicks}__"
        last_click = time.time()
        clicks = 0

    ctx.element.text = f"TIME: {time.time() - last_click:.1f}"

@click_me.on_click
async def on_click(ctx: quack.EventContext) -> None:
    global clicks
    clicks += 1
    ctx.element.text = f"**CLICK ME! {clicks}**"
    click_me.pos = (500 - click_me.get_rect().width) // 2, 250

app.run()
