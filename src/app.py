import os
import pygame
import threading

from variables import *
from scripts.player import Player
from scripts.human import Human
from scripts.building import Building
from scripts.tilemap import *
from scripts.camera import Camera
from scripts.gui import Canvas, Text, Button
from scripts.graphics.tiles import Loader

class Map:
    def __init__(self, app, pos):
        self.app = app
        self.pos = pos
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 41600, 20800)

class ProgressBar:
    def __init__(self, app, pos, size, border, barColor, max):
        self.app = app
        self.image = pygame.Surface(size)
        self.rect = self.image.get_rect()
        self.bar = pygame.Surface(size)
        self.image_bg = pygame.Surface(size)
        self.image_bg.fill((0,0,0))
        self.rect.topleft = pos
        self.pos = pos
        self.size = size
        self.border = border
        self.bar_color = barColor
        self.max = max
        pygame.draw.rect(self.image, (255,0,0), [self.pos[0], self.pos[1], self.max, self.size[1]])
        self.image.fill(barColor)
    
    def update(self, current):
        percent_of_bar = (current / 14000) * 100
        progress = 9 * int(percent_of_bar) 
        self.app.display.fill((255,255,255))
        self.bar.fill((0,0,0))
        self.image = pygame.transform.scale(self.image, (progress, self.size[1]))
        self.image.fill(self.bar_color)
        self.app.display.blit(self.image_bg, self.rect.topleft)
        self.app.display.blit(self.image, self.rect.topleft)
    
    def draw(self):
        pygame.display.flip()


class App:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        flags = pygame.DOUBLEBUF | pygame.HWSURFACE
        self.width, self.height = 1024, 720
        self.display = pygame.display.set_mode((self.width, self.height), flags, 8)
        self.display.fill((255,255,255))
        pygame.display.flip()

        self.font = pygame.font.Font(None, 20)
        self.loading_font = pygame.font.Font(None, 35)
        self.info_list = {"version": "proof-of-concept"}
        self.fps = 400
        self.ownership_of_sprite = None
        self.start()

    def get_info(self):
        for i, key in enumerate(self.info_list):
            text = self.font.render(str(key) + " : " + str(self.info_list[key]), True, (255,255,255), (0,0,0))
            text_rect = text.get_rect()
            text_rect.y = 20 * i
            self.display.blit(text, text_rect)
    
    def loading_info(self, info):
        text = self.loading_font.render(info, True, (0,0,0), (255,255,255))
        text_rect = text.get_rect()
        text_rect.x = 370
        text_rect.y = 460
        self.display.blit(text, text_rect)
        pygame.display.flip()

    def start(self):
        pos = (67, 500)
        size = (900, 40)
        border = (0,0,0)
        barColor = (0,128,0)
        max_a = 900
        self.info_thread = "no info"
        t1 = threading.Thread(target=self.generate)
        self.loading_bar(t1, pos, size, border, barColor, max_a)
        self.setAllowedEvents()

    def loading_bar(self, thread, pos, size, border, barC, max_progress):
        thread.start()
        bar = ProgressBar(self, pos, size, border, (0,128,0), max_progress)
        current = 0
        while thread.is_alive():
            print(current)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            current += 10
            # print(self.info_thread)
            bar.update(current)
            self.loading_info(self.info_thread)
            bar.draw()
        bar.update(10000)
        bar.draw()
        time.sleep(1)

    def generate(self):
        start = time.perf_counter()
        self.optimize = True
        self.loader = Loader()
        self.info_thread = "generating sprites.."
        self.sprites_group = pygame.sprite.Group()
        self.chunks_group = pygame.sprite.LayeredUpdates()
        self.builds_group = pygame.sprite.Group()
        self.canvas_group = pygame.sprite.Group()
        self.tiles_group = pygame.sprite.Group()
        self.info_thread = "loading sprites.."
        self.player = Player(self.sprites_group, (0,0), (25,25), (0,0,255))
        self.human = Human(self, self.sprites_group, "test_1")
        self.info_thread = "generating random map data.."
        self.visible_chunks = []
        if self.optimize: self.map_data = generate_map_with_mpp()
        else: self.map_data = generate_map()
        self.info_thread = "generating chunks.."        
        self.chunks = generate_chunk(self.chunks_group, self.tiles_group, generate_map(), 1)
        self.empty_chunks = generate_chunk(self.chunks_group, self.tiles_group, generate_map(1), 2, True)
        self.chunks_list = [self.chunks, self.empty_chunks]
        self.camera = Camera(self.human, self.width, self.height, self.chunks_group)
        self.map_rect = Map(self, (0,0))
        self.building_canvas = Canvas(self, (48,500), (900,200), None, 255, (101,67,33))
        # self.building_canvas.add_text("hello ...")
        self.building_canvas.add_button("house", (5,5), (90,30), (255,255,255))
        self.building_canvas.add_button("tree", (5,40), (90,30), (255,255,255))
        self.building = Building(self)

        self.is_collide_to_chunk = False

        # self.e1 = Entity(self.sprites_group, (50,50))
        finish = time.perf_counter()
        print("optimized: {1} - Time of execution {0} seconds".format(round(finish-start, 3), self.optimize))


    def setAllowedEvents(self):
        pygame.event.set_allowed([pygame.QUIT, pygame.K_a, pygame.K_b])

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    if self.building.active: self.building.active = False
                    else: self.building.active = True


    def button_controller(self):
        if self.building_canvas.button_objs[0].clicked: 
            self.building.building_type = "house"
        if self.building_canvas.button_objs[1].clicked: 
            self.building.building_type = "tree"

    def draw(self):
        self.display.fill((0,0,0))
        draw_map(self, self.display, self.chunks_list, self.camera)
        # draw_map(self, self.display, self.empty_chunks, self.camera)
        self.building.draw()
        for sprite in self.sprites_group:
            self.display.blit(sprite.image, sprite.rect.topleft + self.camera.offset)
        # self.canvas_group.draw(self.display)
        self.get_info()
    
    def change_ownership(self):
        for sprite in self.canvas_group:
            if sprite.rect.collidepoint(self.mouse_pos):
                self.ownership_of_sprite = sprite
            else:
                self.ownership_of_sprite = None

    def update(self):
        self.buttons = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.change_ownership()
        self.camera.show_position()
        self.camera.scroll()
        self.camera.update()
        self.building.update()
        self.sprites_group.update()
        self.canvas_group.update()
        self.update_infos()        
        self.button_controller()

    def update_infos(self):
        self.info_list["building"] = self.building.active
        self.info_list["chunk_pos"] = self.building.chunk_pos
        self.info_list["tile_pos"]  = self.building.tile_pos
        self.info_list["FPS"] = self.clock.get_fps()
       
    def execute(self):
        self.running = 1
        while self.running:
            self.dt = self.clock.tick(60) / 1000
            self.handle_event()
            self.update()
            self.draw()
            pygame.display.flip()
        pygame.quit()
    
    def quit(self):
        pygame.quit()

pygame.quit()