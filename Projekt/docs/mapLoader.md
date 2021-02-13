# mapLoader

Class that is responsible for map handling. It loads map from .tmx files, I used Tiled program for making maps, all tiles are in Assets/Maps/Tiles.tsx file.

### Constants

| Name  | Description	|
| :------------ |:---------------:|
| FIRST_LEVEL_PATH| Path to map of first level|
| SECOND_LEVEL_PATH| Path to map of second level|


### Methods

| Name  | Description	|
| :------------ |:---------------:|
| __init__(self,  width, height, window)| Initialize object, initialize necessary sprite lists|
| load_level(self, level_index)| Load level and all sprite lists from it|
| draw_level(self)| Draws all map layers, order of drawing is important|