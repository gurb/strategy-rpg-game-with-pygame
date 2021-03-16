import pygame
from pygame import Vector2

from scripts.graphics.texture import *
from utils.colors import *
## 48x48


class BodyPart:
    def __init__(self, w, h, color, pos, angle):
        self.image = pygame.Surface([w,h], pygame.SRCALPHA)
        self.image.fill(color)
        self.pos = pos
        self.rect = self.image.get_rect()
        self.angle = angle
        self.image = pygame.transform.rotate(self.image, self.angle)
        self.pos = pos
    
    def update(self):
        self.image = pygame.transform.rotate(self.image, self.angle)

COLOR = BLACK

idle = {
    "head"  : BodyPart(8,8, COLOR, (20,4), 0),
    "chest" : BodyPart(16,16,COLOR, (16,13), 0),
    "top_arm_1"   : BodyPart(2, 8, COLOR, (12,13), 0),
    "top_arm_2"   : BodyPart(2, 8, COLOR, (34,13), 0),
    "bottom_arm_1": BodyPart(2, 8, COLOR, (12,20), 0),
    "bottom_arm_2": BodyPart(2, 8, COLOR, (34,20), 0),
    "top_leg_1"   : BodyPart(2, 10, COLOR, (19,31), 0),
    "top_leg_2"   : BodyPart(2, 10, COLOR, (27,31), 0),
    "bottom_leg_1": BodyPart(2, 8, COLOR, (19,38), 0),
    "bottom_leg_2": BodyPart(2, 8, COLOR, (27,38), 0),
}

run_1 = {
    "head"  : BodyPart(8,8, COLOR, (20,4), 0),
    "chest" : BodyPart(16,16,COLOR, (16,13), 0),
    "top_arm_1"   : BodyPart(2, 8, COLOR, (12,13), 0),
    "top_arm_2"   : BodyPart(2, 8, COLOR, (34,13), 0),
    "bottom_arm_1": BodyPart(2, 8, COLOR, (12,20), 0),
    "bottom_arm_2": BodyPart(2, 8, COLOR, (34,20), 0),
    "top_leg_1"   : BodyPart(3, 10, COLOR, (19,31), -30),
    "top_leg_2"   : BodyPart(3, 10, COLOR, (27,31), 30),
    "bottom_leg_1": BodyPart(2, 8, COLOR, (19,38), -60),
    "bottom_leg_2": BodyPart(2, 8, COLOR, (27,38), -30),
}

class Human(pygame.sprite.Sprite):
    def __init__(self, sprites_group, name, w=48, h=48):
        self.groups = sprites_group
        pygame.sprite.Sprite.__init__(self, self.groups)
        self.name = name
        self.image = pygame.Surface([w, h], pygame.SRCALPHA)


        self.merge_parts(self.image, run_1)

        # self.image = pygame.transform.scale(self.image, (24,24))
        self.rect = self.image.get_rect()
        self.pos = Vector2(250,250)
        self.rect.topleft = (250, 250)
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



