import time
import quack

app = quack.App((700, 700), tick=165)
app.set_background_colour(20, 20, 20)

app.clicks = 0
app.last_click = time.time()

cps_box = app.add_rect(app.get_size(), colour=(255, 255, 0), border_width=4, border_radius=10)

click_text = app.add_text(
    "**CLICK!** ",
    100,
    colour=(255, 255, 0),
)

click_text.apply_animation(quack.AnimationType.HOVER_DIM, 0.5)
click_text.center()

cps_text = app.add_text("**YOUR CPS IS: 0**", 50, colour=(255, 255, 0))

cps_text_rect = app.add_rect(
    (cps_text.get_width() + 45, cps_text.get_height() + 10),
    colour=(255, 255, 0),
    border_width=2,
    border_radius=10,
)

cps_text_rect.set_pos(quack.ElementPosType.CENTER, 13)
cps_text.center(cps_text_rect)

image = app.add_image("example_apps/data/test_image.png", (10, 10))
image.resize(100, 100)
image.set_alpha(169)


@cps_box.on_tick
async def on_tick(ctx: quack.EventContext) -> None:
    current_time = time.time()

    if current_time - ctx.app.last_click >= 1 and ctx.app.clicks > 0:
        cps_text.text = f"**YOUR CPS IS: {ctx.app.clicks}**"
        click_text.text = f"**CLICK!**"

        click_text.center()
        cps_text.center_x()

        ctx.app.clicks = 0
        ctx.app.last_click = time.time()


@cps_box.on_click
async def on_click(ctx: quack.EventContext) -> None:
    ctx.app.clicks += 1
    click_text.text = f"**CLICK! {ctx.app.clicks}**"
    click_text.center()


app.run()
