import pygame
import os

class Build(pygame.sprite.Sprite):
    def __init__(self, builds_group, pos):
        self.groups = builds_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.pos = pos
        self.type = 0 # house as default
        self.rect = pygame.Rect(self.pos[0], self.pos[1], 32, 32)

class Building:
    def __init__(self, app):
        self.app = app
        self.buildings = {
            0 : {
                "type"      : "house",
                "counter"   : 0,
                "image"     : pygame.image.load(os.path.join(os.path.dirname(__file__), 'graphics','house.png')),
                "size"      : 4
            }
        }
        self.active = False
         # default

    def update(self):
        if self.active:
            self.build()

    def build(self):
        pos = pygame.mouse.get_pos()
        buttons = pygame.mouse.get_pressed()
        print(buttons)
        # Check if the rect collided with the mouse pos
        # and if the left mouse button was pressed.
        if buttons[0]:
            mouse_pos = pygame.mouse.get_pos()
            pure = mouse_pos[0] // 64
            mouse_x = pure * 64
            pure = mouse_pos[1] // 32
            mouse_y = pure * 32
            print("olustu")
            Build(self.app.builds_group, (mouse_x, mouse_y))

    def draw(self):
        for sprite in self.app.builds_group:
            self.app.display.blit(
                self.buildings[sprite.type]["image"],
                (sprite.pos[0], sprite.pos[1])
            )