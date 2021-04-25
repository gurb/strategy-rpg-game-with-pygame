# 🎮 THE RPG GAME
[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/rQO1Pm8-Dx0/0.jpg)](https://www.youtube.com/watch?v=rQO1Pm8-Dx0)

This project's aim is making a game as rpg and strategy on the open world. 
The game map's generated via perlin noise like nature of the world. Some op-
timizations are implemented to the game to obtain better performance. 


## 📅 to do list
- ❌ reduce the CPU usage of the game (the RAM usage seems stable) 
- ❌ loading screen
- ❌ auto-tiling
- ❌ add a minimap when will open the character moved
- 🔃 add some buildings and trees(collideable) (as generated)
- 🔃 add gui (canvas, text, button)
- ❌ add inventory

## 📝building system 
- we can use mask for each chunk and we could make it tileable building on the map
- when mouse clicking is collided choosen color, the map coordinate will be defined 
- if color red then map_data = [(chunk.x * 10) + red.x, (chunk.y * 10) + red.y] = some_building_asset

## 📝layered tilemap
- if building system has to work, the feature of layered tilemap is necessary at this point
- I suppose the map_data can be manipulated at the running time of the prototype
- the information of the map needed, is already got by building system (tile_pos, chunk_pos)

## 📝aseprite notes
* tree: 1px spray 6 9


