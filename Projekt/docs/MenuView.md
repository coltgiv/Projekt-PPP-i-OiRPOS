# MenuView

Class that is showed at the beginning of game, inherits from arcade.View.

### Methods

| Name  | Description	|
| :------------ |:---------------:|
| __init__(self,  width, height, window)| Initialize object, saves passed parameters.|
| on_show(self)| Setting background color|
| on_draw(self)| Drawing texts in window|
| on_mouse_press(self, x, y, button, modifiers)| When LMB is pressed create game view and show it|