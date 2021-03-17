import pygame

from scripts.player import Player
from scripts.human import Human
from scripts.building import Building
from scripts.tilemap import *
from scripts.camera import Camera

class App:
    def __init__(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.display = pygame.display.set_mode((1024, 720))
        
    def generate(self):
        self.sprites_group = pygame.sprite.Group()
        self.chunks_group = pygame.sprite.Group()
        self.builds_group = pygame.sprite.Group()
        self.player = Player(self.sprites_group, (0,0), (25,25), (0,0,255))
        self.human = Human(self.sprites_group, "test_1")
        self.chunks = generate_chunk(self.chunks_group, generate_map())
        self.camera = Camera(self.human, 640, 480, self.chunks_group)
        self.building = Building(self)


    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_b:
                    print("basti")
                    if self.building.active: self.building.active = False
                    else: self.building.active = True

    def draw(self):
        self.display.fill((0,0,0))
        draw_map(self.display, self.chunks, self.camera)
        self.building.draw()
        for sprite in self.sprites_group:
            self.display.blit(sprite.image, (sprite.rect.topleft + self.camera.offset))

    def update(self):
        self.camera.show_position()
        self.camera.scroll(0.05)
        self.camera.update()
        self.building.update()
        self.sprites_group.update()

    def execute(self):
        self.running = True
        while self.running:
            self.clock.tick(60)
            self.handle_event()
            self.draw()
            self.update()
    
            pygame.display.flip()
    
    def quit(self):
        pygame.quit()

pygame.quit()