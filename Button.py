import pygame, os, random

class Button:
    def __init__(self, text, text_color, background_color, width, height, pc_x, pc_y, font_size=36, font_type="Consolas"):
        self.text = str(text)
        self.text_color = text_color
        self.background_color = background_color
        self.width = width
        self.height = height
        self.font_size = font_size
        self.font_type = font_type
        self.font = pygame.font.SysFont(self.font_type, self.font_size)
        self.pc_x = pc_x
        self.pc_y = pc_y
        self.update()

    def update(self):
        self.image = self.font.render(self.text, True, self.text_color)
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.pc_x, self.pc_y
        self.text_rect = self.image.get_rect(center=self.rect.center)

    def draw(self, surface):
        surface.fill(self.background_color, self.rect)
        surface.blit(self.image, self.text_rect)

