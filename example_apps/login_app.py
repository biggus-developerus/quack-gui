import quack

app = quack.App((500, 500))

app.set_background_colour(15, 15, 15)

login_text = app.add_header_text("Login", colour=(255, 10, 40))
login_text.set_pos(quack.ElementPosType.CENTER, quack.ElementPosType.TOP + 50)

username_inp = app.add_inputbox((250, 50), colour=(255, 10, 40), border_radius=10)
username_inp.set_pos(quack.ElementPosType.CENTER, quack.ElementPosType.CENTER)

# TODO: Placeholder text & password input (hide the password being written)
# TODO: Probably handle held keys asw... sob x69420

password_inp = app.add_inputbox((250, 50), colour=(255, 10, 40), border_radius=10)
password_inp.set_pos(quack.ElementPosType.CENTER, quack.ElementPosType.CENTER + (username_inp.get_height() + 10))

submit_btn = app.add_button("Submit", (100, 50), colour=(255, 10, 40), border_radius=10)
submit_btn.set_pos(quack.ElementPosType.CENTER, quack.ElementPosType.CENTER + ((username_inp.get_height() + 10) + (password_inp.get_height() + 30)))

@submit_btn.on_click
async def submit_form(ctx: quack.EventContext) -> None:
    if not username_inp._user_text.text or not password_inp._user_text.text:
        return
    
    ctx.app._elements.clear()

    title = app.add_header_text(f"Welcome back {username_inp._user_text.text}!", colour=(10, 255, 40))
    title.set_pos(quack.ElementPosType.CENTER, quack.ElementPosType.TOP + 50)

app.run()