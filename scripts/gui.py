import pygame

class Canvas(pygame.sprite.Sprite):
    def __init__(self, app, pos, size, texture=None, opacity=255, color=(0,0,0)):
        self.app = app
        pygame.sprite.Sprite.__init__(self, app.canvas_group)
        self.opacity = opacity
        if texture:
            self.texture = texture
            self.image = self.texture
        else:
            self.image = pygame.Surface(size, pygame.SRCALPHA)
            self.image.fill(color+tuple([opacity]))

        self.relative_pos = None

        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.rect.size = size

        self.text_objs = []
        self.button_objs = []

        self.font = self.app.font

        self.change_status = True

        self.pos = pos
        self.color = color

    def add_text(self, text_data):
        self.text_objs.append(Text(self.app, text_data, 13, (0,0,0)))
        self.change_status = True
        self.redraw()

    def add_button(self, button_label, pos, size, bg_color):
        self.button_objs.append(Button(self, button_label, pos, size, bg_color))
        self.change_status = True
        self.redraw()

    def redraw(self):
        if self.change_status:
            self.image.fill(self.color)
            for txt in self.text_objs:
                self.image.blit(txt.text, txt.text_rect)
            for btn in self.button_objs:
                self.image.blit(btn.image, btn.rect)
        else: 
            self.change_status = False

    def update(self):
        for btn in self.button_objs:
            btn.update()

    def draw(self):
        self.app.display.blit(self.image, self.rect.topleft)

class Text:
    def __init__(self, parent, text_data, font_size, font_color, font_type=None, font_path=None, centered=False):
        self.parent = parent
        self.text_data = text_data
        self.font_size = font_size
        self.font_color = font_color
        if font_type: self.font_type = font_type
        if font_path: self.font_path = font_path
        self.font = pygame.font.Font(None, 30)
        # self.font = self.parent.font
        self.text = self.font.render(self.text_data, True, self.font_color)
        self.text_rect = self.text.get_rect()
        self.text_rect.x = self.parent.rect.size[0]/2 - self.text_rect.size[0]/2
        self.text_rect.y = self.parent.rect.size[1]/2 - self.text_rect.size[1]/2

        self.text_pos = [0,0]

class Button:
    def __init__(self, parent, label, pos, size, bg_color, text_color=(0,0,0)):
        self.parent = parent
        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.topleft = pos
        self.rect.size = size
        self.clicked = False
        text_obj = Text(self, label, 13, text_color)
        self.image.fill(bg_color)
        self.image.blit(text_obj.text, text_obj.text_rect.topleft)
        
        self.real_rect = self.image.get_rect()
        self.real_rect.topleft = (pos[0] + self.parent.pos[0], pos[1] + self.parent.pos[1])
        self.real_rect.size = size

    def update(self):
        if self.parent.app.buttons[0] and self.real_rect.collidepoint(self.parent.app.mouse_pos):
            self.clicked = True
        else:
            self.clicked = False