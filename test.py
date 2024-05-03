import quack
import colorsys

h, s, v = 0, 1, 1
h_inc, s_inc, v_inc = True, True, True


quack.init()

app = quack.App(500, 500, tick=60)
app.set_background_colour(20, 20, 20)

text = app.add_text(
    "**_KEEWL PROXY_**",
    30,
    (175, 10),
)

fps_text = app.add_text(
    "**FPS - {}**",
    40,
    (0, 0)
)

app.add_inputbox((300, 30), (100, 250), border_width=3, border_radius=0)
app.add_inputbox((300, 30), (100, 300), border_width=3)

async def cool_cb(app: quack.App) -> None:
    global h, s, v, h_inc, s_inc, v_inc


    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    r = int(r * 255)
    g = int(g * 255)
    b = int(b * 255)

    fps_text.text = "**FPS - {}**".format(int(app.get_fps()))
    fps_text.colour = (r, g, b)
    text.colour = (r, g, b)

    if h >= 1:
        h_inc = False
    if s >= 0.8:
        s_inc = False
    if v >= 0.8:
        v_inc = False

    if h <= 0:
        h_inc = True
    if s <= 0.5:
        s_inc = True
    if v <= 0.5:
        v_inc = True

    h = h + 0.01 if h_inc else h - 0.01
    s = s + 0.01 if s_inc else s - 0.01
    v = v + 0.01 if v_inc else v - 0.01

app.add_pre_draw_cb(cool_cb)
app.run()

