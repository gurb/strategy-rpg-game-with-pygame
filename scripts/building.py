import pygame
import os

from scripts.tilemap import gen_visible_chunks, settings

from pygame.math import Vector2

    
class Building:
    def __init__(self, app):
        self.app = app
        self.buildings = {
            0 : {
                "type"      : "house",
                "counter"   : 0,
                "image"     : pygame.image.load(os.path.join(os.path.dirname(__file__), 'graphics','house.png')),
                "size"      : 4
            },
            1 : {
                "type"      : "tree",
                "counter"   : 0,
                "image"     : pygame.image.load(os.path.join(os.path.dirname(__file__), 'graphics','tree.png')),
                "size"      : 4
            }
        }
        self.active = False
        self.active_chunk_mask = None
        self.active_rect = None
        # default
        self.building_type = "house"

        self.mouse_pos = None

        self.selected_chunk = pygame.Surface((640, 320), pygame.SRCALPHA)
        self.s_chunk_rect = self.selected_chunk.get_rect()
        self.choosen_rect = None

        self.selected_area = pygame.Surface((64,32), pygame.SRCALPHA)
        self.selected_rect = self.selected_area.get_rect()

        self.useless_selected_area = pygame.Surface((64,32), pygame.SRCALPHA)
        self.useless_selected_rect = self.useless_selected_area.get_rect()

        self.visible_chunks = []
        self.chunk_area = pygame.Surface((640, 384), pygame.SRCALPHA)

        self.mask_selected = pygame.image.load(os.path.join(os.path.dirname(__file__), 'graphics', 'mask.png'))
        self.chunk_mask = pygame.image.load(os.path.join(os.path.dirname(__file__), 'graphics', 'chunk_mask.png'))
        
        pygame.draw.polygon(self.selected_area, (0,255,0), ((0,16),(32,0),(64,16),(32,32)),2)
        pygame.draw.polygon(self.useless_selected_area, (255,0,0), ((0,16),(32,0),(64,16),(32,32)),2)
        
        self.tile_pos = None
        self.chunk_pos = None
        self.relative_tile_position = None

        self.color = None

    def update(self):
        if self.active:
            # self.build()
            self.select()
            self.effect()
            self.build()

    def build(self):
        buttons = pygame.mouse.get_pressed()
        if buttons[0] and self.relative_tile_position and self.chunk_pos:
            pos_0 = self.relative_tile_position[0]
            pos_1 = self.relative_tile_position[1]
            print(str(self.chunk_pos) + str(self.relative_tile_position))
            self.app.empty_chunks[(int(self.chunk_pos[1]),int(self.chunk_pos[0]))][pos_0][pos_1] = self.building_type
            print(str(self.chunk_pos) + str(self.relative_tile_position))
    
    def effect(self):
        self.chunk_area.fill((0,0,0,0)) # clear the chunk area
        scr_x = (self.relative_tile_position[1] * settings["tile_size"]/2) - (self.relative_tile_position[0] * settings["tile_size"]/2) - 320
        scr_y = (self.relative_tile_position[1] * settings["tile_size"]/4) + (self.relative_tile_position[0] * settings["tile_size"]/4)
        # pygame.draw.rect(self.chunk_area, (0,255,255), pygame.Rect(-scr_x-32, scr_y, 64, 32))
        if self.app.empty_chunks[(int(self.chunk_pos[1]),int(self.chunk_pos[0]))][self.relative_tile_position[0]][self.relative_tile_position[1]] != "empty":
            self.chunk_area.blit(self.useless_selected_area, (-scr_x-32, scr_y))
        else:
            self.chunk_area.blit(self.selected_area, (-scr_x-32, scr_y))
        # self.app.display.blit(self.chunk_area, self.choosen_rect.topleft + self.app.camera.offset)

    def select(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.visible_chunks_masks = gen_visible_chunks(self.app.visible_chunks)
        self.screen_to_world = Vector2(self.mouse_pos[0] - self.app.camera.offset.x, self.mouse_pos[1] - self.app.camera.offset.y)

        # print(self.screen_to_world)
        for surface, rect, chunk_pos in self.visible_chunks_masks[1]:
            if rect.collidepoint(self.screen_to_world):
                self.relative_offset = ((self.mouse_pos[0] - rect.x - int(self.app.camera.offset.x))%640, (self.mouse_pos[1] - rect.y - int(self.app.camera.offset.y))%320)
                color = surface.get_at(self.relative_offset)
                if color == (255,0,0,255) or color == (0,0,255,255) or color == (255,255,0,255) or color == (0,255,0,255): pass
                else:
                    self.color = surface.get_at(self.relative_offset)
                    self.chunk_pos = chunk_pos
                    self.choosen_rect = rect
                    self.relative_tile_position = (settings["colors_pos"][self.color[:3]][0], settings["colors_pos"][self.color[:3]][1])
                    self.tile_pos =  (
                                        self.chunk_pos[0] * 10 + settings["colors_pos"][self.color[:3]][0],
                                        self.chunk_pos[1] * 10 + settings["colors_pos"][self.color[:3]][1]
                                    )

    def draw(self):
        if self.choosen_rect:
            self.app.display.blit(self.chunk_area, self.choosen_rect.topleft + self.app.camera.offset)
