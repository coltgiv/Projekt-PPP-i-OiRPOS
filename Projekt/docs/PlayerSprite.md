# PlayerSprite

Class that is responsible for setting player sprite and animations.

### Constants

| Name  | Description	|
| :------------ |:---------------:|
| SCALING| Scale of loaded pictures|
| RIGHT_DIRECTION| Parameter for direction|
| LEFT_DIRECTION| Parameter for direction|
| UPDATES_PER_FRAME| Used for slowing changes of texture|

### Methods

| Name  | Description	|
| :------------ |:---------------:|
| __init__(self)| Initialize object, load all textures|
| update_animation(self, delta_time=1 /60)| Depending on player movement and direction change sprite|
