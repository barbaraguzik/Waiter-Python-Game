import pygame, os, random

class Waiter(pygame.sprite.Sprite):
    def __init__(self, waiterImages, cx, cy, images, iceCreamImages, width, height, black, correctSound, wrongSound, checkCollides):
        super().__init__()
        self.waiterImages = waiterImages
        self.image = images['WAITERR']
        self.rect = self.image.get_rect(center=(cx, cy))
        self.step_index = self.points = self._count = 0
        self.lives = 3
        self.steps_right = ['WAITERS1R', 'WAITERR', 'WAITERS2R', 'WAITERR']
        self.steps_left = ['WAITERS1L', 'WAITERL', 'WAITERS2L', 'WAITERL']
        self.horizontal_direction = 'RIGHT'
        self.holding_ice_cream = self.current_flavor = self.text = None
        self.toppings, self.text_time = [], None
        self.text_font = pygame.font.SysFont(None, 36)
        self.images = images
        self.width = width
        self.height = height
        self.black = black
        self.iceCreamImages = iceCreamImages
        self.correct = correctSound
        self.wrong = wrongSound
        self.checkCollides = checkCollides

    def draw(self, surface):
        surface.blit(self.image, self.rect)
        if self.holding_ice_cream:
            if self.horizontal_direction == 'LEFT':
                ice_cream_pos = (self.rect.centerx + 20, self.rect.top)
            else:
                ice_cream_pos = (self.rect.centerx - 70, self.rect.top)
            surface.blit(self.holding_ice_cream, ice_cream_pos)
        if self.text:
            message_surf = self.text_font.render(self.text, True, (255, 0, 0))
            surface.blit(message_surf, (self.rect.centerx - 30, self.rect.top - 40))
        for i in range(self.lives):
            surface.blit(self.images['LIFE'], (400 + i * 65, 0))
        points_surf = self.text_font.render(f'Points: {self.points}', True, self.black)
        surface.blit(points_surf, (620, 40))

    def update(self, key_pressed, obiekty):
        self.get_event(key_pressed)

        if self.rect.bottom > self.height:
            self.rect.bottom = self.height
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if self.rect.centerx > self.width:
            self.rect.centerx = self.width

        if any(key_pressed):
            self._count += 1
            if self._count % 10 == 0:
                self.step_index = (self.step_index + 1) % 4
                if self.horizontal_direction == 'RIGHT':
                    self.image = self.waiterImages[self.steps_left[self.step_index]]
                else:
                    self.image = self.waiterImages[self.steps_right[self.step_index]]
        else:
            if self.horizontal_direction == 'RIGHT':
                self.image = self.waiterImages['WAITERL']
            else:
                self.image = self.waiterImages['WAITERR']
            self.step_index = 0

        if self.text and pygame.time.get_ticks() - self.text_time > 2000:
            self.text = None

    def get_event(self, key_pressed):
        move_x, move_y = 0, 0
        if key_pressed[pygame.K_a]:
            move_x = -4
            self.horizontal_direction = "RIGHT"
        if key_pressed[pygame.K_d]:
            move_x = 4
            self.horizontal_direction = "LEFT"
        if key_pressed[pygame.K_w]:
            move_y = -4
        if key_pressed[pygame.K_s]:
            move_y = 4

        self.move_and_check_collision(move_x, move_y)
    def move_and_check_collision(self, move_x, move_y, ):
        self.rect.x += move_x
        self.rect.y += move_y

        collided = self.checkCollides(self)

        if collided:
            self.rect.x -= move_x
            self.rect.y -= move_y

        if self.rect.bottom > self.height:
            self.rect.bottom = self.height
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if self.rect.centerx > self.width:
            self.rect.centerx = self.width

    def pick_ice_cream(self, ice_cream_image, flavor):
        if self.holding_ice_cream is None:
            if 'SPRINKLES' in flavor or 'ICING' in flavor:
                pass
            else:
                self.holding_ice_cream = ice_cream_image
                self.current_flavor = flavor
                self.toppings = []

        else:
            if 'SPRINKLES' in flavor or 'ICING' in flavor:
                if self.holding_ice_cream:
                    topping_type = flavor.split('_')[-1]
                    if topping_type not in self.toppings:
                        self.toppings.append(topping_type)
                        new_flavor = self.current_flavor
                        if 'SPRINKLES' in new_flavor or 'ICING' in new_flavor:
                            new_flavor = new_flavor.split('_')[0]
                        for topping in sorted(self.toppings):
                            new_flavor += f'_{topping}'
                        if new_flavor in self.iceCreamImages:
                            self.holding_ice_cream = self.iceCreamImages[new_flavor]
                            self.current_flavor = new_flavor

            else:
                if 'SPRINKLES' in self.current_flavor or 'ICING' in self.current_flavor:
                    self.current_flavor = flavor

                else:
                    self.holding_ice_cream = ice_cream_image
                    self.current_flavor = flavor
                    self.toppings = []




    def drop_ice_cream(self):
        self.holding_ice_cream = self.current_flavor = None
        self.toppings = []

    def deliver_order(self, tables):
        if self.holding_ice_cream:
            for table in tables:
                if self.rect.colliderect(table.get_expanded_rect()):
                    if table.bubble and self.current_flavor == table.correct_flavor:
                        self.points += 10
                        table.clear_order()
                        self.text = 'CORRECT'
                        self.correct.play()
                    else:
                        self.lives -= 1
                        self.text = 'WRONG'
                        self.wrong.play()
                        table.clear_order()
                    self.text_time = pygame.time.get_ticks()
                    self.drop_ice_cream()

                    break

    def is_in_selection_area(self, selection_area):
        return self.rect.colliderect(selection_area.rect)
