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

EMPTY_TEXTURE = pygame.Surface((64,32))
EMPTY_TEXTURE.set_colorkey((0,0,0))

def generate_tex_new_version():
    surf = pygame.surface((64,32))
    surf.fill((0,0,0))
    surf = pygame.draw.polygon(surf, (0,255,0), ((0,16),(32,0),(64,16),(32,32)))
    return surf


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
                        color = 0x60683a # color = 0x78955A
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
    foo = pygame.Surface((64,64))
    foo.set_colorkey((0,0,0))
    foo.blit(iso_pixel, (0,32))
    pygame.image.save(iso_pixel, "iso.png")

    if is_rect:
        surf_rect = iso_pixel.get_rect()
        surf_rect.x = pos[0]
        surf_rect.y = pos[1]
        return (iso_pixel, surf_rect)
    else:
        return foo


def generate_tex(texture=None, color_m=None, pixels_len=16, pixel_size=4, is_rect=False, smooth_val = 125, pos = (0,0), obj_array=None, alpha=False):
    if alpha:
        surf = pygame.Surface([pixels_len, pixels_len])
        surf.fill((255,255,255))
    else:
        surf = pygame.Surface([pixels_len, pixels_len])
    pixel_array = pygame.PixelArray(surf)
    alpha_pixel = False
    for col in range(16):
        for row in range(16):
            if texture:
                if texture == _textures['grass']:
                    color = 0x78955A
                if texture == _textures['dirt']:
                    color = 0x9b7653
                if texture == _textures['brick']:
                    color = 0xB53A15
                    if col % 4 == 1:
                        color = 0xBCAFA5 # Beige brick spacing
            elif obj_array is not None:
                if obj_array[col][row] == 11:
                    color = 0x000000
                    alpha_pixel = False
                if obj_array[col][row] == 100:
                    alpha_pixel = True
            elif color_m:
                color = color_m

            if not alpha_pixel:
                red     = (((color >> 16) & 0xff) * random.randint(smooth_val,255)//255) << 16
                green   = (((color >> 8)  & 0xff) * random.randint(smooth_val,255)//255) << 8
                blue    = (((color >> 0)  & 0xff) * random.randint(smooth_val,255)//255)

                color = red | green | blue

                pixel_array[row][col] = int(hex(color), 16)

    # get a new surface that consist from pixel_array
    surf = pixel_array.make_surface()
    surf.set_colorkey((255,255,255))
    # 16x16 -> pixel_size * 16 x pixel_size * 16
    surf = pygame.transform.scale(surf, (pixels_len*pixel_size, pixels_len*pixel_size))
    if is_rect:
        surf_rect = surf.get_rect()
        surf_rect.x = pos[0]
        surf_rect.y = pos[1]
        return (surf, surf_rect)
    else:
        return surf

# if __name__ == "__main__":
#     t = Test(640, 480)
#     t.bg_color = (255,255,255)
#     surf = generate_tex_new_version()
#     surf_pos = (40, 40)
    
#     tex_1 = (surf, surf_pos) 
#     t.add_surface(tex_1)

#     while True:
#         t.loop()