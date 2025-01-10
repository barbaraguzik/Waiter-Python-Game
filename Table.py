import pygame, os, random
from Item import Item

class Table(Item):
    def __init__(self, image, cx, cy, initial_delay, waiter, images, iceCreamImages):
        super().__init__(image, cx, cy)
        self.bubble = self.exclamation = self.correct_flavor = None
        self.bubble_time = self.initial_time = pygame.time.get_ticks()
        self.initial_delay = initial_delay
        self.waiter = waiter
        self.images = images
        self.iceCreamImages = iceCreamImages
    def draw(self, surface):
        super().draw(surface)
        if self.bubble:
            surface.blit(self.images['BUBBLE'], (self.rect.centerx - 50, self.rect.top - 60))
            surface.blit(self.bubble, (self.rect.centerx - 30, self.rect.top - 60))
        if self.exclamation:
            surface.blit(self.exclamation, (self.rect.centerx + 10, self.rect.top - 50))

    def clear_order(self):
        self.bubble = self.exclamation = self.correct_flavor = None
        self.initial_time = pygame.time.get_ticks()

    def set_bubble(self, bubble):
        self.bubble, self.bubble_time = pygame.transform.scale(bubble, (
        int(bubble.get_width() * 0.8), int(bubble.get_height() * 0.8))), pygame.time.get_ticks()
        self.exclamation = None

    def update(self):
        current_time = pygame.time.get_ticks()
        elapsed_time_since_start = current_time - self.initial_time

        if elapsed_time_since_start >= self.initial_delay:
            if self.bubble is None and self.exclamation is None:
                new_flavor = random.choice(list(self.iceCreamImages.keys()))
                self.set_bubble(self.iceCreamImages[new_flavor])
                self.correct_flavor = new_flavor

            if self.bubble:
                elapsed_time = current_time - self.bubble_time
                if elapsed_time > 10000 and self.exclamation is None:
                    self.exclamation = self.images['EXCLAMATION']
                if elapsed_time > 17000:
                    self.clear_order()
                    self.waiter.lives -= 1
                    self.waiter.text = "TOO LATE"
                    self.waiter.text_time = pygame.time.get_ticks()

    def get_expanded_rect(self):
        return self.rect.inflate(40, 40)