import os
import pygame
from pygame.math import Vector2
import random
import math

from scripts.graphics.tiles import *
from scripts.algorithms.perlin import Noise

from utils.funcs import get_info

CHUNK_LEN = 10
TILE_SIZE = 64

settings = {
    "screen_width" : 640,
    "screen_height" : 480,
    "chunk_len" : CHUNK_LEN,
    "tile_size" : TILE_SIZE,                # 64
    "tile_area" : pygame.Surface((64, 64), pygame.SRCALPHA),
    "tile_surface" : pygame.Surface((64, 64)),
    "chunk_size" : TILE_SIZE * CHUNK_LEN,   # 256
    "chunks_x_axis" : 640 / (3 * 64),
    "chunks_y_axis" : 480 / (3 * 64),
    "chunk_surfaces" : pygame.Surface((TILE_SIZE * CHUNK_LEN, TILE_SIZE * CHUNK_LEN)),    
    "chunk_area" : pygame.Surface((640, 320)),
    "chunk_mask": pygame.Surface((640, 320)),
    "colors_pos": {},
    "chunk_mask_image": pygame.image.load(os.path.join(os.path.dirname(__file__), 'graphics', 'chunk_mask.png'))    
}
# dimension of each tiles
# TILE_SIZE = 16

# texture of colors
YELLOW  = (255, 255, 0)
RED     = (255, 0, 0)
BLUE    = (0 , 0, 255)
GREEN   = (0, 255, 0)
BROWN   = (160, 82, 45)
BLACK   = (0, 0, 0)
DARK_GRAY   = (32,32,32,60)

pygame.draw.polygon(settings["tile_area"], DARK_GRAY, (
    (0, 48),
    (32,32),
    (64, 48),
    (32, 64)
    ),1
)

def get_tile_surface(color_m, pos):
    xy = (color_m[1] + color_m[2]) % 255
    color = (color_m[1],color_m[2],xy)
    settings["colors_pos"][color] = pos
    pygame.draw.polygon(settings["tile_surface"], color, (
        (0, 48),
        (32, 32),
        (64, 48),
        (32, 64)
        )
    )
    return settings["tile_surface"]


def create_mask():
    surf = pygame.Surface((64,64))
    for y in range(10):
        for x in range(10):
            scr_x = (y * settings["tile_size"]/2) - (x * settings["tile_size"]/2)
            scr_y = (y * settings["tile_size"]/4) + (x * settings["tile_size"]/4)

            settings["chunk_mask"].blit(get_tile_surface((y,scr_x%255,scr_y%255),(y,x)), (scr_x + (settings["chunk_size"]/2 - 32), scr_y))
    return settings["chunk_mask"]


settings["chunk_mask"] = create_mask()
for key in settings["colors_pos"]:
    print("key[{0}] : {1}".format(key, settings["colors_pos"][key]))
pygame.image.save(settings["chunk_mask"], "chunk_mask.png")


def draw_grid():
    for y in range(10):
        for x in range(10):
            scr_x = (y * settings["tile_size"]/2) - (x * settings["tile_size"]/2)
            scr_y = (y * settings["tile_size"]/4) + (x * settings["tile_size"]/4)
            settings["chunk_area"].blit(settings["tile_area"], (scr_x + (settings["chunk_size"]/2 - 32), scr_y))
            pygame.image.save(settings["chunk_area"], "grid_mask.png")

# draw_grid()
    
pygame.draw.polygon(settings["chunk_area"], (0,255,0), (
    (0, 160),
    (320,0),
    (640, 160),
    (320, 320)
    ),1
)

class Chunk(pygame.sprite.Sprite):
    def __init__(self, chunks_group, pos, layer, camera=None):
        self._layer = layer
        self.groups = chunks_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = Vector2(pos[0], pos[1])
        self.x = (pos[1] * settings["chunk_size"]/2) - (pos[0] * settings["chunk_size"]/2) - settings["tile_size"]/2 + 20800
        self.y = (pos[1] * settings["chunk_size"]/4) + (pos[0] * settings["chunk_size"]/4)
        self.rect = pygame.Rect(self.x, self.y, settings["chunk_size"], settings["chunk_size"]/2)
        self.collide_visible = False
        self.visible = False

class Tile(pygame.sprite.Sprite):
    def __init__(self, tiles_group, pos, camera=None):
        self.groups = tiles_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = Vector2(pos[0], pos[1])
        self.x = (pos[1] * settings["tile_size"]/2) - (pos[0] * settings["tile_size"]/2) - 32 + 20800
        self.y = (pos[1] * settings["tile_size"]/4) + (pos[0] * settings["tile_size"]/4)
        self.rect = pygame.Rect(self.x, self.y, settings["tile_size"], settings["tile_size"]/2)
        self.collide_visible = False
        self.visible = False

def mask_chunk(x, y):
    return [
        [(x-2, y-2), (x-1, y-2), (x, y-2), (x+1, y-2), (x+2, y-2)],
        [(x-2, y-1), (x-1, y-1), (x, y-1), (x+1, y-1), (x+2, y-1)],
        [(x-2, y),  (x-1, y), (x, y), (x+1, y), (x+2, y)],
        [(x-2, y+1), (x-1, y+1), (x, y+1), (x+1, y+1), (x+2, y+1)],
        [(x-2, y+2), (x-1, y+2), (x, y+2), (x+1, y+2), (x+2, y+2)]        
    ]

def generate_chunk(chunks_group, tiles_group, map_data, layer, empty=False):
    chunks = {}
    # length of tiles in width
    len_tiles_w = len(map_data[0])
    len_chunks_w = len_tiles_w // settings["chunk_len"]
    # length of tiles in height
    len_tiles_h = len(map_data)
    len_chunks_h = len_tiles_h // settings["chunk_len"]

    for c_y in range(len_chunks_w):
        chunk_data = []            
        for c_x in range(len_chunks_h):
            key = (c_x, c_y)
            Chunk(chunks_group, key, layer)

            chunks[key] = []
    for key in chunks:
        for y in range(settings["chunk_len"]):
            row = []
            for x in range(settings["chunk_len"]):
                tile_position = (key[0] * settings["chunk_len"] + x, key[1] * settings["chunk_len"] + y)
                if empty: row.append('empty') # it is just for the creating an empty map
                else: row.append(map_data[tile_position[1]][tile_position[0]])
            chunks[key].append(row)

        # create chunk

    # for key, value in chunks.items():
    #     chunks[key] = get_chunk_surface(chunks[key])
    if empty:
        for key, value in chunks.items():
            print(str(key) + ": " + str(value))
        
    return chunks

def genNoise(x, y):
    value = 0
    value += Noise(x * 0.005, y * 0.005) * 1.0
    value += Noise(x * 0.025, y * 0.025) * .5 
    value += Noise(x * 0.05, y * 0.05) * 0.25
    # print("sdfdsf")
    # print(value)
    return value

def generate_map(tile_amount=650, tilesize = TILE_SIZE, freq=0.01, amp=0.5):
    tile = None
    map_data = []
    for i in range(tile_amount):
        map_data.append([])
        for j in range(tile_amount):
            # n = Noise(i*freq, j*freq) * amp
            n = genNoise(i, j)
            # if n >= 0.7 and n < 1.0:
            if n < -0.05:
                map_data[i].append('water')
            # n >= 0.65 and n < 0.7
            elif n < 0.0:
                map_data[i].append('l_water')
            # elif n >= 0.6 and n < 0.65:
            elif n < 0.05:
                map_data[i].append('dirt')
            else:
                map_data[i].append('grass')
            # convert to hex from string value

    return map_data

def get_chunk_surface(chunk, layer=0):
    settings["chunk_surfaces"].fill((0,0,0))
    for y, row in enumerate(chunk):
        for x, tile in enumerate(row):
            scr_x = (y * settings["tile_size"]/2) - (x * settings["tile_size"]/2)
            scr_y = (y * settings["tile_size"]/4) + (x * settings["tile_size"]/4) + 32
            settings["chunk_surfaces"].blit(textures[tile][0], (scr_x + (settings["chunk_size"]/2 - 32), scr_y))
            # if layer == 0: 
            #     settings["chunk_surfaces"].blit(settings["tile_area"], (scr_x + (settings["chunk_size"]/2 - 32), scr_y))

            # tile grid
     
    settings["chunk_surfaces"].set_colorkey((0,0,0))
    return settings["chunk_surfaces"]

def draw_map(app, screen, chunks_list, camera = None):
    target_pos = camera.focus_chunk.pos
    app.visible_chunks = mask_chunk(target_pos.x, target_pos.y)
    
    for row in mask_chunk(target_pos.x, target_pos.y):
        for pos in row:
            if pos[0] > -1 and pos[1] > -1 and pos[0] < 65 and pos[1] < 65:
                scr_x = (pos[1] * settings["chunk_size"]/2) - (pos[0] * settings["chunk_size"]/2) - 320 + 20800
                scr_y = (pos[1] * settings["chunk_size"]/4) + (pos[0] * settings["chunk_size"]/4)
                # layer 0 of the map
                screen.blit(get_chunk_surface(chunks_list[0][pos[0],pos[1]], 0),
                            (scr_x + camera.offset.x, scr_y + camera.offset.y))
                # layer 1 of the map
                screen.blit(get_chunk_surface(chunks_list[1][pos[0],pos[1]], 1),
                            (scr_x + camera.offset.x, scr_y + camera.offset.y))
                # pygame.image.save(get_chunk_surface(chunks[pos[0],pos[1]]), "chunk_image.png")
                # screen.blit(settings["chunk_area"], (scr_x + camera.offset.x, scr_y + camera.offset.y))

def gen_visible_chunks(chunks):
    visible_chunks_list = []
    visible_chunks_masks_list = []
    for row in chunks:
        for pos in row:
            if pos[0] > -1 and pos[1] > -1 and pos[0] < 65 and pos[1] < 65:
                scr_x = (pos[1] * settings["chunk_size"]/2) - (pos[0] * settings["chunk_size"]/2) - 320 + 20800
                scr_y = (pos[1] * settings["chunk_size"]/4) + (pos[0] * settings["chunk_size"]/4)
                chunk_rect = settings["chunk_area"].get_rect()
                chunk_rect.x = scr_x
                chunk_rect.y = scr_y + 64 # this 32 is using for the offset of the height 64px, example 64x64
                visible_chunks_list.append((settings["chunk_area"], chunk_rect))
                visible_chunks_masks_list.append((settings["chunk_mask_image"], chunk_rect, (pos[1], pos[0])))
    return (visible_chunks_list, visible_chunks_masks_list)