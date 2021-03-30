import os
import pygame

from variables import *
from scripts.player import Player
from scripts.human import Human
from scripts.building import Building
from scripts.tilemap import *
from scripts.camera import Camera

class Entity(pygame.sprite.Sprite):
    def __init__(self, sprite_groups, pos):
        self.groups = sprite_groups
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.type = 1 # tree as default
        self.image = pygame.Surface([10, 10])
        self.image.fill((255,0,0))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos

class Map:
    def __init__(self, app, pos):
        self.app = app
        self.pos = pos
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 41600, 20800)
        
class App:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((1024, 720))
        self.font = pygame.font.Font(None, 20)
        self.info_list = {"version": "proof-of-concept"}
        self.fps = 400

    def get_info(self):
        for i, key in enumerate(self.info_list):
            text = self.font.render(str(key) + " : " + str(self.info_list[key]), True, (255,255,255), (0,0,0))
            text_rect = text.get_rect()
            text_rect.y = 20 * i
            self.display.blit(text, text_rect)

    def generate(self):
        self.sprites_group = pygame.sprite.Group()
        self.chunks_group = pygame.sprite.LayeredUpdates()
        self.builds_group = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.player = Player(self.sprites_group, (0,0), (25,25), (0,0,255))
        self.human = Human(self.sprites_group, "test_1")
        self.visible_chunks = []
        self.chunks = generate_chunk(self.chunks_group, self.tiles_group, generate_map(), 1)
        self.empty_chunks = generate_chunk(self.chunks_group, self.tiles_group, generate_map(), 2, True)
        self.chunks_list = [self.chunks, self.empty_chunks]
        self.camera = Camera(self.human, 1024, 720, self.chunks_group)
        self.map_rect = Map(self, (0,0))
        self.building = Building(self)

        self.is_collide_to_chunk = False

        self.e1 = Entity(self.sprites_group, (50,50))

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    if self.building.active: self.building.active = False
                    else: self.building.active = True

    def draw(self):
        self.display.fill((0,0,0))
        draw_map(self, self.display, self.chunks_list, self.camera)
        # draw_map(self, self.display, self.empty_chunks, self.camera)
        self.building.draw()
        for sprite in self.sprites_group:
            self.display.blit(sprite.image, sprite.rect.topleft + self.camera.offset)
        self.get_info()
    def update(self):
        self.camera.show_position()
        self.camera.scroll()
        self.camera.update()
        self.building.update()
        self.sprites_group.update()
        self.update_infos()        

    def update_infos(self):
        self.info_list["building"] = self.building.active
        self.info_list["chunk_pos"] = self.building.chunk_pos
        self.info_list["tile_pos"]  = self.building.tile_pos
        self.info_list["FPS"] = self.clock.get_fps()
       
    def execute(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick() / 1000
            self.handle_event()
            self.draw()
            self.update()
    
            pygame.display.flip()
    
    def quit(self):
        pygame.quit()

pygame.quit()