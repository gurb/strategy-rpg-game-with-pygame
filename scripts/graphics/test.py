import pygame

class Test:
    def __init__(self, width, height):
        pygame.init()
        self.display = pygame.display.set_mode([width, height])
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("test")
        self.sprites = pygame.sprite.Group()
        self.surfaces = []
        self.bg_color = ((0,0,0))
        self.running = True
        self.FPS = 60

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.quit()
    
    def add_surface(self, surf):
        self.surfaces.append(surf)

    def update(self):
        self.sprites.update()

    def draw(self):
        self.display.fill(self.bg_color)
        for surf in self.surfaces:
            self.display.blit(surf[0], surf[1])
        self.sprites.draw(self.display)
        pygame.display.flip()
    
    def loop(self):
        while self.running:
            self.clock.tick(self.FPS)
            self.event()
            self.draw()
            self.update()