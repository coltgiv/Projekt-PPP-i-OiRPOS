import arcade
from MenuView import MenuView

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 512
SCREEN_TITLE = "Projekt"

def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    menu_View = MenuView(SCREEN_WIDTH, SCREEN_HEIGHT, window)
    window.show_view(menu_View)
    arcade.run()


if __name__ == "__main__":
    main()