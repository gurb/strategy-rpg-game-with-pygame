import pygame
import random

# texture of colors
YELLOW  = 0xffff00
RED     = 0xff0000
BLUE    = 0xff
GREEN   = 0xff00
BROWN   = 0x9b7653
GRASS   = 0x567d46
WATER   = 0x4040ff
L_WATER = 0x6666fb

settings_t = {
    "two_pos" : [14, 17]
}
_textures = {
    'grass' : 0x6772617373,
    'dirt'  : 0x64697274a,
    'brick' : 0x627269636b
}

def generate_texture_with_pixels(width, height):
    surf = pygame.Surface((32,16))
    surf.fill((0,0,0))
    pixel_array = pygame.PixelArray(surf)
    for col in range(16):
        if col > 8:
            settings_t["two_pos"][0] += 2
            settings_t["two_pos"][1] -= 2
        for row in range(32):
            if settings_t["two_pos"][0] <= row and settings_t["two_pos"][1] >= row:
                pixel_array[row][col] = int(hex(0x9b7653), 16)
        if 0 <= col and col < 7:
            settings_t["two_pos"][0] -= 2
            settings_t["two_pos"][1] += 2
    surf = pixel_array.make_surface()
    surf = pygame.transform.scale(surf, (width, height))
    surf.set_colorkey((0,0,0))
    return surf

def generate_iso_tex(texture=None, color_m=None, w=16, h=8, is_rect=False, pos=(0,0), smooth_val=230):
    iso_pixel = generate_texture_with_pixels(w, h)
    pixel_array = pygame.PixelArray(iso_pixel)
    # print("pixel_value : {0}".format(pixel_array[0][0]))
    
    for col in range(h):
        for row in range(w):
            if iso_pixel.get_at((row, col))[:3] != (0,0,0):
                if texture:
                    if texture == _textures['grass']:
                        color = 0x78955A
                    if texture == _textures['dirt']:
                        color = 0x9b7653
                if color_m:
                    color = color_m 
                red     = (((color >> 16) & 0xff) * random.randint(smooth_val,255)//255) << 16
                green   = (((color >> 8)  & 0xff) * random.randint(smooth_val,255)//255) << 8
                blue    = (((color >> 0)  & 0xff) * random.randint(smooth_val,255)//255)
                color = red | green | blue
                # print(color)
                pixel_array[row][col] = int(hex(color), 16)
    # print("pixels_length : {0}".format())

    iso_pixel = pixel_array.make_surface()
    iso_pixel = pygame.transform.scale(iso_pixel, (64, 32))
    iso_pixel.set_colorkey((0,0,0))
    if is_rect:
        surf_rect = iso_pixel.get_rect()
        surf_rect.x = pos[0]
        surf_rect.y = pos[1]
        return (iso_pixel, surf_rect)
    else:
        return iso_pixel  