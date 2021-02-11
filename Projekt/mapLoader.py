import arcade

FIRST_LEVEL_PATH = "Assets/Maps/FirstLevel.tmx"
SECOND_LEVEL_PATH = "Assets/Maps/SecondLevel.tmx"
class mapLoader():
    def __init__(self):
        self.map = None
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.finish_list = arcade.SpriteList()
        self.deadly_objects = arcade.SpriteList()
        self.background_objects = arcade.SpriteList()
        self.background_images = arcade.SpriteList()

    def load_level(self, level_index):
        if level_index == 1:
            self.map = arcade.tilemap.read_tmx(FIRST_LEVEL_PATH)
        elif level_index == 2:
            self.map = arcade.tilemap.read_tmx(SECOND_LEVEL_PATH)
        if self.map != None:
             self.wall_list = arcade.tilemap.process_layer(self.map, "Ground", 0.5)
             self.coin_list = arcade.tilemap.process_layer(self.map, "Coins", 0.5)
             self.finish_list = arcade.tilemap.process_layer(self.map, "Finish", 0.5)
             self.deadly_objects = arcade.tilemap.process_layer(self.map, "DeadlyObjects", 0.5)
             self.background_objects = arcade.tilemap.process_layer(self.map, "BackgroundObjects", 0.5)
             self.background_images = arcade.tilemap.process_layer(self.map, "Background", 0.5)
    def draw_level(self):
        self.background_images.draw()
        self.background_objects.draw()
        self.deadly_objects.draw()
        self.wall_list.draw()
        self.finish_list.draw()
        self.coin_list.draw()