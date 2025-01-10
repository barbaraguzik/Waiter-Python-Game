import pygame, os, random
from Item import Item

class Container(Item):
    def __init__(self, image, cx, cy, flavor):
        super().__init__(image, cx, cy)
        self.original_image = image
        self.enlarged_image = pygame.transform.scale(image,(int(image.get_width() * 1.1), int(image.get_height() * 1.1)))
        self.flavor = flavor

    def draw(self, surface):
        super().draw(surface)

    def enlarge(self):
        self.image, self.rect = self.enlarged_image, self.enlarged_image.get_rect(center=self.rect.center)

    def shrink(self):
        self.image, self.rect = self.original_image, self.original_image.get_rect(center=self.rect.center)