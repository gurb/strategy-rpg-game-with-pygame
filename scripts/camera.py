import pygame
from pygame.math import Vector2

class Camera:
    def __init__(self, target, width, height, chunks_group):
        self.width = width
        self.height = height
        self.camera = Vector2(target.pos.x, target.pos.y)
        self.target = target
        self.offset = Vector2(0,0)
        self.focus_chunk = None
        self.chunks_group = chunks_group
        for chunk in self.chunks_group:
            # print(chunk.pos)
            if self.target.rect.colliderect(chunk.rect):
                self.focus_chunk = chunk

    def scroll(self, smooth=1):
        self.pointTarget = self.target.pos - self.camera
        self.camera += self.pointTarget * smooth
        self.offset = -self.camera + Vector2(self.width/2, self.height/2)
        
        # limit scrolling to map size
        self.offset.x = min(0,self.offset.x) # left
        self.offset.y = min(0,self.offset.y) # top
        self.offset.x = max(-41600 + self.width, self.offset.x) 
        self.offset.y = max(-20800 + self.height, self.offset.y) 

    def show_position(self):
        # print("camera: {0}".format(-self.offset))
        # print("player: {0}".format(self.target.pos))
        pass

    def update(self):
        if self.target.is_move:
            for chunk in self.chunks_group:
                if self.target.rect.colliderect(chunk.rect):
                    if chunk.pos != self.focus_chunk.pos:
                        self.focus_chunk.visible = False
                        chunk.visible = True
                        self.focus_chunk = chunk
                        break