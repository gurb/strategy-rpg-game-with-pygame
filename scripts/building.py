import pygame
import os

from scripts.tilemap import gen_visible_chunks, settings

from pygame.math import Vector2

class Build(pygame.sprite.Sprite):
    def __init__(self, builds_group, pos):
        self.groups = builds_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.type = 1 # tree as default
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 32, 32)
        self.rect.midtop = self.pos
        
        # tiles effect

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
        self.building_type = "tree"

        self.mouse_pos = None
        self.cell = None
        self.offset = None

        self.selected_chunk = pygame.Surface((640, 320), pygame.SRCALPHA)
        self.s_chunk_rect = self.selected_chunk.get_rect()

        self.selected_area = pygame.Surface((64,32), pygame.SRCALPHA)
        self.selected_rect = self.selected_area.get_rect()

        self.visible_chunks = []
        self.chunk_area = pygame.Surface((640, 320), pygame.SRCALPHA)

        self.mask_selected = pygame.image.load(os.path.join(os.path.dirname(__file__), 'graphics', 'mask.png'))
        self.chunk_mask = pygame.image.load(os.path.join(os.path.dirname(__file__), 'graphics', 'chunk_mask.png'))


        self.tile_pos = None
        self.chunk_pos = None
        self.relative_tile_position = None

        self.color = None

    def update(self):
        if self.active:
            # self.build()
            self.select()
            self.build()

    def build(self):
        buttons = pygame.mouse.get_pressed()
        if buttons[0] and self.relative_tile_position and self.chunk_pos:
            pos_0 = self.relative_tile_position[0]
            pos_1 = self.relative_tile_position[1]
            print(str(self.chunk_pos) + str(self.relative_tile_position))
            self.app.empty_chunks[(int(self.chunk_pos[1]),int(self.chunk_pos[0]))][pos_0][pos_1] = self.building_type
            print(str(self.chunk_pos) + str(self.relative_tile_position))

    # def effect(self):
    #     if self.relative_tile_position and self.chunk_pos:
    #         self.selected_rect.x = 
    #         self.app.display.blit(self.selected_area, ())

    def select(self):
        self.mouse_pos = pygame.mouse.get_pos()
        self.visible_chunks = gen_visible_chunks(self.app.visible_chunks)
        self.visible_chunks_masks = gen_visible_chunks(self.app.visible_chunks)
        self.screen_to_world = Vector2(self.mouse_pos[0] - self.app.camera.offset.x, self.mouse_pos[1] - self.app.camera.offset.y)

        # print(self.screen_to_world)
        self.cell = [self.mouse_pos[0] // 640, self.mouse_pos[1] // 320]
        self.offset = (self.mouse_pos[0] % 640, self.mouse_pos[1] % 320)
        for surface, rect, chunk_pos in self.visible_chunks_masks[1]:
            if rect.collidepoint(self.screen_to_world):
                self.relative_offset = ((self.mouse_pos[0] - rect.x - int(self.app.camera.offset.x))%640, (self.mouse_pos[1] - rect.y - int(self.app.camera.offset.y))%320)
                color = surface.get_at(self.relative_offset)
                if color == (255,0,0,255) or color == (0,0,255,255) or color == (255,255,0,255) or color == (0,255,0,255): pass
                else:
                    self.color = surface.get_at(self.relative_offset)
                    self.active_chunk_mask = surface
                    self.active_rect = rect
                    # print(str(self.color) + str(settings["colors_pos"][self.color[:3]]))
                    self.chunk_pos = chunk_pos
                    self.relative_tile_position = (settings["colors_pos"][self.color[:3]][0], settings["colors_pos"][self.color[:3]][1])
                    self.tile_pos =  (
                                        self.chunk_pos[0] * 10 + settings["colors_pos"][self.color[:3]][0],
                                        self.chunk_pos[1] * 10 + settings["colors_pos"][self.color[:3]][1]
                                    )
        
        



        
    # def build(self):
    #     self.mouse_pos = pygame.mouse.get_pos()
    #     self.screen_to_world = (self.mouse_pos[0] + 20800, self.mouse_pos[1])
    #     if self.app.camera.focus_chunk.rect.collidepoint(self.screen_to_world):
    #         print("hit GREEN")
            
    #     self.cell = [self.mouse_pos[0] // 64, self.mouse_pos[1] // 32]
    #     self.offset = (self.mouse_pos[0] % 64, self.mouse_pos[1] % 32)

    #     color = self.mask_selected.get_at(self.offset)

    #     x_offset = 0
    #     y_offset = 0

    #     if color == (255,0,0,255):
    #         x_offset = -32
    #         y_offset = -16
    #     if color == (0,0,255,255):
    #         x_offset = +32
    #         y_offset = -16
    #     if color == (255,255,0,255):
    #         x_offset = -32
    #         y_offset = +16
    #     if color == (0,255,0,255):
    #         x_offset = +32
    #         y_offset = +16

    #     pygame.draw.polygon(self.selected_area, (0,255,0), (
    #         (0, 16),
    #         (32,0),
    #         (64, 16),
    #         (32, 32)
    #         ),1
    #     )

    #     pygame.draw.polygon(self.chunk_area, (0,255,0), (
    #         (0, 160),
    #         (320,0),
    #         (640, 160),
    #         (320, 320)
    #         ),1
    #     )
    #     self.app.display.blit(self.active_chunk_mask, self.active_rect)

    #     print("chunk_pos: {0}, mouse_pos: {1}".format(self.app.camera.focus_chunk.rect.topleft, self.mouse_pos))

    #     self.s_x = (self.cell[0] * 64) + x_offset
    #     self.s_y = (self.cell[1] * 32) + y_offset
    #     self.selected_pos = Vector2(self.s_x, self.s_y)
    #     self.selected_rect = pygame.Rect(self.cell[0] * 64, self.cell[1] * 32 ,64,32)
    #     pygame.draw.rect(self.selected_area, (255,0,0), self.selected_rect, 2)
        
    #     self.app.display.blit(self.chunk_area, (self.app.camera.focus_chunk.rect.x + self.app.camera.offset.x - 320, self.app.camera.focus_chunk.rect.y + self.app.camera.offset.y))
    #     self.app.display.blit(self.selected_area, self.selected_pos)

    #     buttons = pygame.mouse.get_pressed()

    #     # print(buttons)
    #     # Check if the rect collided with the mouse pos
    #     # and if the left mouse button was pressed.
    #     if buttons[0]:
    #         mouse_pos = pygame.mouse.get_pos()
    #         pure = mouse_pos[0] // 64
    #         mouse_x = pure * 64
    #         pure = mouse_pos[1] // 32
    #         mouse_y = pure * 32
    #         print("olustu")
    #         Build(self.app.builds_group, self.selected_pos)

    def draw(self):
        for sprite in self.app.builds_group:
            self.app.display.blit(
                self.buildings[sprite.type]["image"],
                (sprite.rect.x + 20800 + self.app.camera.offset.x, sprite.rect.y + self.app.camera.offset.y)
            )