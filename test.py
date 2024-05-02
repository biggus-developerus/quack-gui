import quack


def main() -> None:
    quack.init()

    app = quack.App(500, 500)

    app.set_background_colour(20, 20, 20)

    app.add_text(
        "_KEEWL PROXY_",
        30,
        (175, 10),
        font=None,
    )

    app.add_inputbox((300, 30), (100, 250), border_width=3)
    app.add_inputbox((300, 30), (100, 300), border_width=3)

    app.run()


if __name__ == "__main__":
    main()
