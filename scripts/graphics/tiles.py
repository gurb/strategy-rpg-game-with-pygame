from scripts.graphics.texture import *
# isometric tiles

YELLOW  = 0xffff00
RED     = 0xff0000
BLUE    = 0xff
GREEN   = 0xff00
BROWN   = 0x9b7653
GRASS   = 0x567d46
WATER   = 0x4040ff
L_WATER = 0x6666fb

iso_grass_tiles     = []
iso_dirt_tiles      = []
iso_water_tiles     = []
iso_l_water_tiles   = []

[iso_grass_tiles.append(generate_iso_tex(None, GRASS, 32, 16, False, (160, 160))) for i in range(100)]
[iso_dirt_tiles.append(generate_iso_tex(None, BROWN, 32, 16, False, (160, 160))) for i in range(100)]
[iso_water_tiles.append(generate_iso_tex(None, WATER, 32, 16, False, (160, 160))) for i in range(100)]
[iso_l_water_tiles.append(generate_iso_tex(None, L_WATER, 32, 16, False, (160, 160))) for i in range(100)]

# print(water_tiles)

textures = {
    "grass"    : iso_grass_tiles,
    "dirt"     : iso_dirt_tiles,
    "water"    : iso_water_tiles,
    "l_water"  : iso_l_water_tiles
}

seed_textures = [random.randint(0, 100) for i in range(100)]
# print(seed_textures)

tiles = [1,2]