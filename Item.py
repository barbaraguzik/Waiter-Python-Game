import pygame

class Item(pygame.sprite.Sprite):
    def __init__(self, image, cx, cy):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(cx, cy))
    def draw(self, surface):
        surface.blit(self.image, self.rect)