# GameView

Class with most game logic.

### Constants

| Name  | Description	|
| :------------ |:---------------:|
| GRAVITY| Defines how strong is gravity|
| MOVEMENT_SPEED| How fast should player move|
| LIFE_AMOUNT| How much lifes does player have|

### Methods

| Name  | Description	|
| :------------ |:---------------:|
| __init__(self,  width, height, window, level, score)| Initialize essential parameters and game engine|
| on_draw(self)| Draws map, player and texts|
| on_key_press(self, key, modifiers)| Controls player movement, there is a cooldown for jumping|
| on_key_release(self, key, modifiers)| Resets player movement speed|
| update(self, delta_time)| Updates game state by checking and handling collisions, also updates camera position|
| check_jumping(self)| Resets value of parameter, used in Timer to implement cooldown for jumping|
| player_died(self)| Called when player died, creates and shows game over view|
| load_new_level(self)| Called when player should start new level|
| player_finished_game(self, finished_time)| Called when player finished whole game|

# GameOverView

View that is showed when player died.

### Methods

| Name  | Description	|
| :------------ |:---------------:|
| __init__(self,  width, height, window)| Initialize object, saves passed parameters.|
| on_show(self)| Setting background color|
| on_draw(self)| Drawing texts in window|
| on_mouse_press(self, x, y, button, modifiers)| When LMB is pressed create new game view and show it|

# NewLevelView

View that is showed when player should start new level.

### Methods

| Name  | Description	|
| :------------ |:---------------:|
| __init__(self,  width, height, window)| Initialize object, saves passed parameters.|
| on_show(self)| Setting background color|
| on_draw(self)| Drawing texts in window|
| on_mouse_press(self, x, y, button, modifiers)| When LMB is pressed create new game view and show it|

# FinishedGameView

View that is showed when player finished whole game.

### Methods

| Name  | Description	|
| :------------ |:---------------:|
| __init__(self,  width, height, window)| Initialize object, saves passed parameters.|
| on_show(self)| Setting background color|
| on_draw(self)| Drawing texts in window|
| on_mouse_press(self, x, y, button, modifiers)| When LMB is pressed create new game view and show it|





