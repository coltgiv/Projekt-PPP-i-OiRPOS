import arcade
import os

SCALING = 0.15
RIGHT_DIRECTION = 0
LEFT_DIRECTION = 1
UPDATES_PER_FRAME = 4

class PlayerSprite(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.direction = RIGHT_DIRECTION
        self.current_texture = 0
        self.scale = SCALING
        path_prefix = "Assets/Character/"
        self.idle_texture = [arcade.Texture] * 2
        self.idle_texture[0] = arcade.load_texture(f"{path_prefix}Idle (1).png")
        self.idle_texture[1] = arcade.load_texture(f"{path_prefix}Idle (1).png", flipped_horizontally=True)
        self.run_textures = []
        for i in range(1, 9):
            texture = [arcade.Texture] * 2
            texture[0] = arcade.load_texture(f"{path_prefix}Run ({i}).png")
            texture[1] = arcade.load_texture(f"{path_prefix}Run ({i}).png", flipped_horizontally=True)
            self.run_textures.append(texture)
    def update_animation(self, delta_time=1 /60):
        if self.change_x < 0 and self.direction == RIGHT_DIRECTION:
            self.direction = LEFT_DIRECTION
        elif self.change_x > 1 and self.direction == LEFT_DIRECTION:
            self.direction = RIGHT_DIRECTION
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.idle_texture[self.direction]
            return
        self.current_texture += 1
        if self.current_texture > 7 * UPDATES_PER_FRAME:
            self.current_texture = 0
        texture_index = self.current_texture // UPDATES_PER_FRAME
        self.texture = self.run_textures[texture_index][self.direction]