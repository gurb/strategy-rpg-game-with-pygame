import pygame
from pygame.math import Vector2
import random
import math

from scripts.graphics.tiles import *
from scripts.algorithms.perlin import Noise

from utils.funcs import get_info

CHUNK_LEN = 8
TILE_SIZE = 64

settings = {
    "screen_width" : 640,
    "screen_height" : 480,
    "chunk_len" : CHUNK_LEN,
    "tile_size" : TILE_SIZE,                # 64
    "chunk_size" : TILE_SIZE * CHUNK_LEN,   # 256
    "chunks_x_axis" : 640 / (3 * 64),
    "chunks_y_axis" : 480 / (3 * 64),
    "chunk_surfaces" : pygame.Surface((TILE_SIZE * CHUNK_LEN, TILE_SIZE/2 * CHUNK_LEN))    
}
# dimension of each tiles
TILE_SIZE = 64

# texture of colors
YELLOW  = (255, 255, 0)
RED     = (255, 0, 0)
BLUE    = (0 , 0, 255)
GREEN   = (0, 255, 0)
BROWN   = (160, 82, 45)

class Chunk(pygame.sprite.Sprite):
    def __init__(self, chunks_group, pos, camera=None):
        self.groups = chunks_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = Vector2(pos[0], pos[1])
        self.x = (pos[1] * settings["chunk_size"]/2) - (pos[0] * settings["chunk_size"]/2) - settings["tile_size"]/2
        self.y = (pos[1] * settings["chunk_size"]/4) + (pos[0] * settings["chunk_size"]/4)
        self.rect = pygame.Rect(self.x, self.y, settings["chunk_size"], settings["chunk_size"]/2)
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

def generate_chunk(chunks_group, map_data):
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
            Chunk(chunks_group, key)
            chunks[key] = []

    for key in chunks:
        y = key[1]
        x = key[0]
        for y in range(settings["chunk_len"]):
            row = []
            for x in range(settings["chunk_len"]):
                tile_position = (key[0] * settings["chunk_len"] + x, key[1] * settings["chunk_len"] + y)
                row.append(map_data[tile_position[1]][tile_position[0]])
            chunks[key].append(row)
        
        # create chunk

    # for key, value in chunks.items():
    #     chunks[key] = get_chunk_surface(chunks[key])

    # for key, value in chunks.items():
    #     print(str(key) + ": " + str(value))
        
    return chunks

# def generate_map():
#     map_data = []
#     tiles = [1, 2]
#     for i in range(500):
#         map_data.append([])
#         for j in range(500):
#             map_data[i].append(tiles[random.randint(0,1)])
#     return map_data

def genNoise(x, y):
    value = 0
    value += Noise(x * 0.005, y * 0.005) * 1.0
    value += Noise(x * 0.025, y * 0.025) * .5 
    value += Noise(x * 0.05, y * 0.05) * 0.25
    # print("sdfdsf")
    # print(value)
    return value

def generate_map(tile_amount=625, tilesize = TILE_SIZE, freq=0.01, amp=0.5):
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

def get_chunk_surface(chunk):
    for y, row in enumerate(chunk):
        for x, tile in enumerate(row):
            scr_x = (y * settings["tile_size"]/2) - (x * settings["tile_size"]/2)
            scr_y = (y * settings["tile_size"]/4) + (x * settings["tile_size"]/4)
            settings["chunk_surfaces"].blit(textures[tile][0], (scr_x + (settings["chunk_size"]/2 - 32), scr_y)) 
    settings["chunk_surfaces"].set_colorkey((0,0,0))
    return settings["chunk_surfaces"].convert()

def draw_map(screen, chunks, camera = None):
    start_x = (camera.target.pos.x) // settings["chunk_size"]
    # we divide it with 2 for isometric
    start_y = (camera.target.pos.y) // settings["chunk_size"]/2

    start_x, start_y = round(start_x), round(start_y)
    
    # get_info(start_x, "start_x")
    # get_info(start_y, "start_y")

    end_x = round(start_x + 640 / settings["chunk_size"])
    end_y = round(start_y + 480 / settings["chunk_size"] / 2)

    # get_info(end_x, "end_x")
    # get_info(end_y, "end_y")

    center_x, center_y = round((start_x + end_x) / 2), round((start_y + end_y) / 2)
    # get_info(center_x, "center_x")
    # get_info(center_y, "center_y")
    
    # get_info(mask_chunk(center_x, center_y), "mask")
    target_pos = camera.focus_chunk.pos
    
    # mask_chunk(x, y)

    for row in mask_chunk(target_pos.x, target_pos.y):
        for pos in row:
            if pos[0] > -1 and pos[1] > -1:
                scr_x = (pos[1] * settings["chunk_size"]/2) - (pos[0] * settings["chunk_size"]/2) - settings["tile_size"]/2
                scr_y = (pos[1] * settings["chunk_size"]/4) + (pos[0] * settings["chunk_size"]/4)
                screen.blit(get_chunk_surface(chunks[pos[0],pos[1]]),
                            (scr_x + camera.offset.x, scr_y + camera.offset.y))

    # for y in range(start_y - 10, start_y + 10):
    #     for x in range(start_x - 10, start_x + 10):
    #         if x > -1 and y > -1:
    #             scr_x = (y * settings["chunk_size"]/2) - (x * settings["chunk_size"]/2) - settings["tile_size"]/2
    #             scr_y = (y * settings["chunk_size"]/4) + (x * settings["chunk_size"]/4)
    #             screen.blit(get_chunk_surface(chunks[x,y]),
    #                         (scr_x + camera.offset.x, scr_y + camera.offset.y))