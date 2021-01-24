import arcade
import random
import os

SPRITE_SCALING_PLAYER = 0.15
SPRITE_SCALING_COIN = 0.25
SPRITE_SCALING_WALL = 0.5
COIN_COUNT = 50
GRAVITY = .15

MOVEMENT_SPEED = 5

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 512
SCREEN_TITLE = "Projekt"

VIEWPORT_MARGIN = SCREEN_WIDTH / 2

class MyGame(arcade.Window):
 
    def __init__(self):
         # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite Lists
        self.player_list = None
        self.coin_list = None
        self.wall_list = None
        self.finish_list = None
        self.deadly_objects = None
        self.background_objects = None
        self.background_images = None

        # Player info and engine
        self.player_sprite = None
        self.score = 0
        self.physics_engine = None

        self.view_left = 0
        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):

        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.finish_list = arcade.SpriteList()
        self.deadly_objects = arcade.SpriteList()
        self.background_objects = arcade.SpriteList()
        self.background_images = arcade.SpriteList()

        self.player_sprite = arcade.Sprite("Assets/Character/Idle.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 192
        self.player_list.append(self.player_sprite)

        my_map = arcade.tilemap.read_tmx("Assets/Maps/FirstLevel.tmx")

        self.wall_list = arcade.tilemap.process_layer(my_map, "Ground", 0.5)
        self.coin_list = arcade.tilemap.process_layer(my_map, "Coins", 0.5)
        self.finish_list = arcade.tilemap.process_layer(my_map, "Finish", 0.5)
        self.deadly_objects = arcade.tilemap.process_layer(my_map, "DeadlyObjects", 0.5)
        self.background_objects = arcade.tilemap.process_layer(my_map, "BackgroundObjects", 0.5)
        self.background_images = arcade.tilemap.process_layer(my_map, "Background", 0.5)

        self.view_left = 0


        #Set up collisions between player and walls
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant=GRAVITY)

    def on_draw(self):
        arcade.start_render()
        self.background_images.draw()
        self.background_objects.draw()
        self.deadly_objects.draw()
        self.wall_list.draw()
        self.finish_list.draw()
        self.coin_list.draw()
        self.player_list.draw()

        output = f"Score: {self.score}"
        arcade.draw_text(output, 10, 20, arcade.color.WHITE, 14)

    
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def update(self, delta_time):
        self.coin_list.update()

        coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list )

        for coin in coin_hit_list:
            coin.remove_from_sprite_lists()
            self.score +=1
        
        changed_View = False

        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary and self.player_sprite.left > 280:
            self.view_left -= left_boundary - self.player_sprite.left
            changed_View = True
        right_boundary = self.view_left + SCREEN_WIDTH - VIEWPORT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed_View = True
        self.view_left = int(self.view_left)
        if changed_View:
                arcade.set_viewport(self.view_left, SCREEN_WIDTH + self.view_left,0 ,SCREEN_HEIGHT)

        self.physics_engine.update()

def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()