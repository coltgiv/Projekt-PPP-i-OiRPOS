import arcade
import random
import os

SPRITE_SCALING_PLAYER = 0.2
SPRITE_SCALING_COIN = 0.25
SPRITE_SCALING_WALL = 0.5
COIN_COUNT = 50
GRAVITY = .45

MOVEMENT_SPEED = 5

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Projekt"

class MyGame(arcade.Window):
 
    def __init__(self):
         # Call the parent class initializer
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Sprite Lists
        self.player_list = None
        self.coin_list = None
        self.wall_list = None

        # Player info and engine
        self.player_sprite = None
        self.score = 0
        self.physics_engine = None

        # Don't show the mouse cursor
        self.set_mouse_visible(False)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):

        self.player_list = arcade.SpriteList()
        self.coin_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()

        self.player_sprite = arcade.Sprite("Assets/Character/Idle.png", SPRITE_SCALING_PLAYER)
        self.player_sprite.center_x = 50
        self.player_sprite.center_y = 64
        self.player_list.append(self.player_sprite)

        #Create random coins
        for i in range(COIN_COUNT):
            coin = arcade.Sprite("Assets/Miscellaneous/coin.png", SPRITE_SCALING_COIN)
            coin.center_x = random.randrange(SCREEN_WIDTH)
            coin.center_y = random.randrange(SCREEN_HEIGHT)

            self.coin_list.append(coin)

        #Create walls just for testing
        for x in range(0, 650, 64):
            wall = arcade.Sprite("Assets/Miscellaneous/tile.png", SPRITE_SCALING_WALL)
            wall.center_x = x
            wall.center_y = 0
            self.wall_list.append(wall)

        for y in range(273, 500, 64):
            wall = arcade.Sprite("Assets/Miscellaneous/tile.png", SPRITE_SCALING_WALL)
            wall.center_x = 465
            wall.center_y = y
            self.wall_list.append(wall)
        
        #Set up collisions between player and walls
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, gravity_constant=GRAVITY)

    def on_draw(self):
        arcade.start_render()
        self.coin_list.draw()
        self.wall_list.draw()
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

        self.physics_engine.update()

def main():
    game = MyGame()
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()