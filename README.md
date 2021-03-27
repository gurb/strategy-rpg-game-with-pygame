# THE RPG GAME
This project's aim is making a game as rpg and strategy on the open world. 
The game map's generated via perlin noise like nature of the world. Some op-
timizations are implemented to the game to obtain better performance. 

## to do list
- reduce the CPU usage of the game (RAM seems stable)
- loading screen
- auto-tiling
- add a minimap when will open the character moved
- add some buildings and trees(collideable) (as generated)
- meta of human .......................................... 0%

## building system 
- we can use mask for each chunk and we could make it tileable building on the map
- when mouse clicking is collided choosen color, the map coordinate will be defined 
- if color red then map_data = [(chunk.x * 10) + red.x, (chunk.y * 10) + red.y] = some_building_asset

## aseprite notes
* tree: 1px spray 6 9


