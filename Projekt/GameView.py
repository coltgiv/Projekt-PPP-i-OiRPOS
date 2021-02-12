import arcade
import random
import os
from mapLoader import mapLoader
from threading import Timer
from PlayerSprite import PlayerSprite
from datetime import datetime
from SoundHandler import SoundHandler

#Constant that define base game mechanics
SPRITE_SCALING_COIN = 0.25
SPRITE_SCALING_WALL = 0.5
GRAVITY = .3
MOVEMENT_SPEED = 5
LIFE_AMOUNT = 3

#Class responsible for game mechanics
class GameView(arcade.View):
    #Initialize parameters
    def __init__(self,  width, height, window, level, score):
        #Screen parameters
        self.screen_width = width
        self.screen_height = height
        self.viewport_margin = self.screen_width / 2
        self.window = window
        # Player sprite lists
        self.player_list = arcade.SpriteList()
        self.player = PlayerSprite()
        # Player info, map and engine
        self.player.center_x = 64
        self.player.center_y = 192
        self.player_list.append(self.player)
        self.score = score
        self.current_level = level;
        self.map = mapLoader()
        self.map.load_level(self.current_level)
        self.is_jumping = False
        self.is_checking_jumping = False
        self.view_left = 0
        self.life_count = 3
        self.last_safe_coord = [0] * 2
        self.last_safe_coord[0] = 64
        self.last_safe_coord[1] = 192
        # Don't show the mouse cursor
        self.window.set_mouse_visible(False)
        #Timer for measuring player time to finish level 
        self.init_time = datetime.now()
        #Sound handler
        self.sound_handler = SoundHandler()
        #Set up background and engine
        arcade.set_background_color(arcade.color.AMAZON)
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.map.wall_list, gravity_constant=GRAVITY) 
    
    def on_draw(self):
        #Draw map and player
        arcade.start_render()
        self.map.draw_level()
        self.player_list.draw()
        #Draw score and life text
        output = f"Score: {self.score}"
        output_x = self.player.center_x-(self.screen_width/3)
        #Text has to move with player, this statement make sure that texts are visible even on the beginning of game.
        if output_x < 128:
            output_x = 128
        arcade.draw_text(output, output_x, 20, arcade.color.WHITE, 14)
        output_life = f"Lifes: {self.life_count}"
        arcade.draw_text(output_life, output_x, 40, arcade.color.WHITE, 14)

    
    def on_key_press(self, key, modifiers):
        #Handle jumping, using timer to make sure that player can't go into space
        if key == arcade.key.UP and self.is_jumping == False:
            self.player.change_y = 1.5*MOVEMENT_SPEED
            self.is_jumping = True
            t = Timer(0.6, self.check_jumping)
            t.start()
        #Handle moving left and right
        elif key == arcade.key.LEFT:
            self.player.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player.change_x = MOVEMENT_SPEED
        
    def on_key_release(self, key, modifiers):
        #Reset player movement speed after key release
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player.change_x = 0

    def update(self, delta_time):
        #Update coin list and player animation
        self.map.coin_list.update()
        self.player_list.update_animation()
        #Check if there is collisions with important sprite lists
        coin_hit_list = arcade.check_for_collision_with_list(self.player, self.map.coin_list )
        killing_object_hit_list = arcade.check_for_collision_with_list(self.player, self.map.deadly_objects)
        finish_object_hit = arcade.check_for_collision_with_list(self.player, self.map.finish_list)

        finished = False
        #If player hit finish line
        if len(finish_object_hit) > 0:
            self.sound_handler.play_sound("NextLevel")
            self.load_new_level()
            finished = True
        #Handle collecting of coins, save position of coin as checkpoint if player dies
        for coin in coin_hit_list:
            self.sound_handler.play_sound("Coin")
            self.last_safe_coord[0] = self.player.center_x
            self.last_safe_coord[1] = self.player.center_y
            coin.remove_from_sprite_lists()
            self.score +=1
        
        changed_View = False
        #Handle camera movement
        left_boundary = self.view_left + self.viewport_margin
        if self.player.left < left_boundary and self.player.left > 280:
            self.view_left -= left_boundary - self.player.left
            changed_View = True
        right_boundary = self.view_left + self.screen_width - self.viewport_margin
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            changed_View = True
        self.view_left = int(self.view_left)
        #Handle player dying
        died = False
        if len(killing_object_hit_list) > 0:
            self.sound_handler.play_sound("Death")
            self.life_count -=  1
            if self.life_count < 0:
                self.player_died()
            self.player.center_x = self.last_safe_coord[0]
            self.player.center_y = self.last_safe_coord[1]
            arcade.set_viewport(0, self.screen_width ,0 ,self.screen_height)
            died = True
        #Update camera and engine
        if changed_View and died == False and finished == False :
                arcade.set_viewport(self.view_left, self.screen_width + self.view_left,0 ,self.screen_height)

        self.physics_engine.update()
        #Method that reset value of jumping parameter
    def check_jumping(self):
        self.is_jumping = False
    #Create and show GameOverView, used when player dies
    def player_died(self):
        game_over_view = GameOverView(self.screen_width, self.screen_height, self.window)
        self.window.show_view(game_over_view)
    #Handle new levels if player should finish game or load new level using new view
    def load_new_level(self):
        self.current_level += 1
        finished_time = datetime.now() - self.init_time
        if self.current_level > 2:
            self.player_finished_game(finished_time)
        else:
            new_level_view = NewLevelView(self.screen_width, self.screen_height, self.window,self.score, self.current_level, finished_time)
            self.window.show_view(new_level_view)
        arcade.set_viewport(0, self.screen_width ,0 ,self.screen_height)
    #Create and show FinishedGameView
    def player_finished_game(self, finished_time):
        finished_game_view = FinishedGameView(self.screen_width, self.screen_height, self.window, finished_time)
        self.window.show_view(finished_game_view)

#View that is showed after player died, used to reset game
class GameOverView(arcade.View):
    #Set up parameters
    def __init__(self,  width, height, window):
        self.width = width
        self.height = height
        self.window = window
        self.window.set_mouse_visible(True)
    #Set up background
    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)
    #Show text
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text("Game Over", self.width/2, self.height/2,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to restart",self.width/2, self.height/2 - 75,
                         arcade.color.WHITE, font_size=20, anchor_x="center" )
    #When mouse is pressed start new game
    def on_mouse_press(self, x, y, button, modifiers):
        game_view = GameView(self.width,self.height, self.window, 1, 0)
        self.window.show_view(game_view)

#View that is showed after player finished level and should start new one
class NewLevelView(arcade.View):
    #Set up parameters and calculate how long it took to beat level
    def __init__(self,  width, height, window, score, level, finished_time):
        self.width = width
        self.height = height
        self.window = window
        self.window.set_mouse_visible(True)
        self.score = score
        self.level = level
        seconds = finished_time.seconds
        minutes = (seconds // 60) % 60
        seconds = seconds % 60
        self.finished_time = str(minutes) + ":" + str(seconds)
    #Set up background
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
    #Set up text
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(f"You finished level in {self.finished_time}", self.width/2, self.height/2,
                         arcade.color.BLACK, font_size=40, anchor_x="center")
        arcade.draw_text("Click to start new level",self.width/2, self.height/2 - 75,
                         arcade.color.BLACK, font_size=20, anchor_x="center" )
    #When mouse is presed start next level
    def on_mouse_press(self, x, y, button, modifiers):
        game_view = GameView(self.width,self.height, self.window, self.level, self.score)
        self.window.show_view(game_view)

#View that is showed after player finished whole game
class FinishedGameView(arcade.View):
    #Set up parameters and calculate how long it took to beat last level
    def __init__(self,  width, height, window, finished_time):
        self.width = width
        self.height = height
        self.window = window
        self.window.set_mouse_visible(True)
        seconds = finished_time.seconds
        minutes = (seconds // 60) % 60
        seconds = seconds % 60
        self.finished_time = str(minutes) + ":" + str(seconds)
    #Set up background
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)
    #Set up texts
    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(f"You finished last level in {self.finished_time}", self.width/2, self.height/2,
                         arcade.color.BLACK, font_size=40, anchor_x="center")
        arcade.draw_text("Click to start new game",self.width/2, self.height/2 - 75,
                         arcade.color.BLACK, font_size=20, anchor_x="center" )
    #When mouse is pressed start new game
    def on_mouse_press(self, x, y, button, modifiers):
        game_view = GameView(self.width,self.height, self.window, 1, 0)
        self.window.show_view(game_view)