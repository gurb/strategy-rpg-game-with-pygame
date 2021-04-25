import os
from scripts.graphics.texture import *
# isometric tiles

YELLOW  = 0xffff00
RED     = 0xff0000
BLUE    = 0xff
GREEN   = 0xff00
BROWN   = 0x9b7653
GRASS   = 0x60683a #0x567d46
L_GRASS = 0x577957
WATER   = 0x4040ff
L_WATER = 0x6666fb

class Loader:
    def __init__(self):
        self.image_stone = pygame.image.load(os.path.join(os.path.dirname(__file__), 'stone.png')).convert_alpha()
        textures["stone"] = [self.image_stone]
        self.image_stone_2 = pygame.image.load(os.path.join(os.path.dirname(__file__), 'stone-2.png')).convert_alpha()
        textures["stone-2"] = [self.image_stone_2]
        self.image_tree_1 = pygame.image.load(os.path.join(os.path.dirname(__file__), 'tree.png')).convert_alpha()
        textures["tree-1"] = [self.image_tree_1]
        self.image_tree_2 = pygame.image.load(os.path.join(os.path.dirname(__file__), 'tree-2.png')).convert_alpha()
        textures["tree-2"] = [self.image_tree_2]
        self.image_pine_1 = pygame.image.load(os.path.join(os.path.dirname(__file__), 'pine.png')).convert_alpha()
        textures["pine"] = [self.image_pine_1]
        self.image_house = pygame.image.load(os.path.join(os.path.dirname(__file__), 'house.png')).convert_alpha()
        textures["house"] = [self.image_house]

        self.image_chunk_filter = generate_tex_with_perlin().convert_alpha()

# image_tree = pygame.image.load(os.path.join(os.path.dirname(__file__), 'tree.png'))
# image_house = pygame.image.load(os.path.join(os.path.dirname(__file__), 'house.png'))

iso_grass_tiles     = []
iso_dirt_tiles      = []
iso_water_tiles     = []
iso_l_water_tiles   = []

# [iso_grass_tiles.append(generate_iso_tex(None, GRASS, 32, 16, False, (160, 160), 255)) for i in range(100)]
# [iso_dirt_tiles.append(generate_iso_tex(None, BROWN, 32, 16, False, (160, 160), 255)) for i in range(100)]
# [iso_water_tiles.append(generate_iso_tex(None, WATER, 32, 16, False, (160, 160), 255)) for i in range(100)]
# [iso_l_water_tiles.append(generate_iso_tex(None, L_WATER, 32, 16, False, (160, 160), 255)) for i in range(100)]

iso_grass_tiles.append(generate_iso_tex(None, L_GRASS, 32, 16, False, (160, 160), 230, True)) 
iso_dirt_tiles.append(generate_iso_tex(None, BROWN, 32, 16, False, (160, 160), 230, True)) 
iso_water_tiles.append(generate_iso_tex(None, WATER, 32, 16, False, (160, 160), 230, True)) 
iso_l_water_tiles.append(generate_iso_tex(None, L_WATER, 32, 16, False, (160, 160), 230, True)) 

# print(water_tiles)



textures = {
    "chunk_filter": [generate_tex_with_perlin()],
    "empty"    : [EMPTY_TEXTURE],
    "grass"    : iso_grass_tiles,
    "dirt"     : iso_dirt_tiles,
    "water"    : iso_water_tiles,
    "l_water"  : iso_l_water_tiles
}
pygame.image.save(iso_grass_tiles[0], "tile_grass.png")
seed_textures = [random.randint(0, 100) for i in range(100)]
# print(seed_textures)

tiles = [1,2]