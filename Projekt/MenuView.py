import arcade
from GameView import GameView

class MenuView(arcade.View):
    def __init__(self,  width, height, window):
        self.window = window
        self.width = width
        self.height = height
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Menu Screen", self.width/2, self.height/2,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to play",self.width/2, self.height/2 - 75,
                         arcade.color.BLACK, font_size=20, anchor_x="center" )
    def on_mouse_press(self, x, y, button, modifiers):
        game_view = GameView(self.width,self.height, self.window, 1, 0)
        self.window.show_view(game_view)