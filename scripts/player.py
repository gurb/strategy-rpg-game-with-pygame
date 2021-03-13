import pygame
import math
from pygame.math import Vector2

class Player(pygame.sprite.Sprite):
    def __init__(self, sprites_group, pos, dim, col):
        self.groups = sprites_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.image = pygame.Surface(dim)
        self.image.fill(col)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.vel = Vector2(0,0)
        self.pos = Vector2(pos)
        self.is_move = False
        self.h = 100

    def cart_to_iso(self, cart):
        if cart.x == 0:
            return Vector2(cart.x - cart.y / 2, cart.x + cart.y / 4) # y-axis movement
        else:
            return Vector2(cart.x/2 - cart.y, cart.x / 4 - cart.y) # x-axis movement
            
    def update(self):
        self.get_event()
        self.rect.center = self.pos

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