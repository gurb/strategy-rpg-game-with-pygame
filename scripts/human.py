import pygame
from pygame import Vector2

from scripts.graphics.texture import *
from utils.colors import *
## 48x48

class Human(pygame.sprite.Sprite):
    def __init__(self, sprites_group, name, w=48, h=48):
        self.groups = sprites_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.name = name
        self.image = pygame.Surface([w, h])
        self.image.set_colorkey(BLACK)
        # self.merge_parts(self.image, run_1)

        # self.image = pygame.transform.scale(self.image, (24,24))
        self.rect = self.image.get_rect()
        self.pos = Vector2(250,250)
        self.pos.x += (20800) 
        self.rect.topleft = (250, 250)
        self.rect.x += 20800
        self.h = 10

        self.is_move = False

    def merge_parts(self, surface, parts):
        for key in parts:
            surface.blit(
                parts[key].image,
                parts[key].pos
            )

    def update(self):
        self.get_event()
        self.rect.topleft = self.pos

    def cart_to_iso(self, cart):
        if cart.x == 0:
            return Vector2(cart.x - cart.y / 2, cart.x + cart.y / 4) # y-axis movement
        else:
            return Vector2(cart.x/2 - cart.y, cart.x / 4 - cart.y) # x-axis movement

    def get_event(self):
        keys = pygame.key.get_pressed()
        is_press = any(keys)
        if keys[pygame.K_w]:
            self.v = self.cart_to_iso(Vector2(0, -self.h))
            self.move(self.v)
        elif keys[pygame.K_s]:
            self.v = self.cart_to_iso(Vector2(0, +self.h))
            self.move(self.v)
        elif keys[pygame.K_a]:
            self.v = self.cart_to_iso(Vector2(-self.h, 0))
            self.move(self.v)
        elif keys[pygame.K_d]:
            self.v = self.cart_to_iso(Vector2(+self.h, 0))
            self.move(self.v)
        if is_press is False:
            self.v = Vector2(0,0)
            self.is_move = False
    
    def move(self, v):
        self.pos.x += v.x
        self.pos.y += v.y
        self.is_move = True