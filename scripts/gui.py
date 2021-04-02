import pygame

class Canvas(pygame.sprite.Sprite):
    def __init__(self, pos, size, texture, color=(0,0,0), opacity=255):
        pygame.sprite.Sprite.__init__(self)
        self.texture = texture
        self.color = color
        self.opacity = opacity

        self.image = self.texture
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.rect.size = size

    def update(self):
        pass

    def draw(self):
        pass
    
class Text:
    def __init__(self):
        pass


class Button:
    def __init__(self):
        pass