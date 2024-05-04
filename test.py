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

quack.Animation.apply_hover_anim(quack.AnimationType.HOVER_DIM, title_text)

app.run()
