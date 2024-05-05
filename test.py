import quack

app = quack.App(500, 500, tick=500)
app.set_background_colour(20, 20, 20)

title_text = app.add_text("**XD**", 50, ((500 - 144) // 2, 10), colour=(255, 255, 0))
title_text.apply_animation(quack.AnimationType.HOVER_DIM, title_text)

app.run()
