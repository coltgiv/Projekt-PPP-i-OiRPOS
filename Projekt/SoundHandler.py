import arcade

class SoundHandler():
    def __init__(self):
        self.death_sound = arcade.load_sound("Assets/Sounds/wolfman.wav")
        self.coin_sound = arcade.load_sound("Assets/Sounds/coin.wav")
        self.next_level_sound = arcade.load_sound("Assets/Sounds/spell.wav")
    def play_sound(self, sound_type):
        if sound_type == "Death":
            arcade.play_sound(self.death_sound)
        elif sound_type == "Coin":
            arcade.play_sound(self.coin_sound)
        elif sound_type == "NextLevel":
            arcade.play_sound(self.next_level_sound)