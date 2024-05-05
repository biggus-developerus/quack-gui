import quack

quack.init()

app = quack.App(500, 500, tick=500)
app.set_background_colour(20, 20, 20)

title_text = app.add_text(
    "**XD**",
    50,
    ((app._screen.get_size()[0] - 144) // 2, 10),
)

quack.Animation.apply_hover_anim(quack.AnimationType.HOVER_DIM, title_text)

app.run()
