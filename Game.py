import pygame, os, random
from Table import Table
from Container import Container
from Item import Item
from Waiter import Waiter
from Button import Button


class Game():
    width = 1000
    height = 560
    imagesPath = "./images/"
    soundsPath = "./sounds/"
    images = {}
    iceCreamImages = {}

    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        self.file_names = os.listdir(self.imagesPath)
        self.firstBackground = pygame.image.load(self.imagesPath + "background.png").convert()
        self.secondBackground = pygame.image.load(self.imagesPath + "background2.png").convert()

        self.darkPink = pygame.Color(209, 146, 197, 255)
        self.lightPink = pygame.Color(230, 193, 222, 255)
        self.black = pygame.Color(0, 0, 0, 255)


        for file_name in self.file_names:
            image_name = file_name[:-4].upper()
            self.images[image_name] = pygame.image.load(self.imagesPath + file_name).convert_alpha()

        self.iceCreamImages = {
            'LEMON': self.images['LEMON'],
            'VANILLA': self.images['VANILLA'],
            'CHOCO': self.images['CHOCO'],
            'STRAWBERRY': self.images['STRAWBERRY'],
            'VANILLA_SPRINKLES': self.images['VANILLA_SPRINKLES'],
            'VANILLA_ICING': self.images['VANILLA_ICING'],
            'VANILLA_ICING_SPRINKLES': self.images['VANILLA_ICING_SPRINKLES'],
            'CHOCO_SPRINKLES': self.images['CHOCO_SPRINKLES'],
            'CHOCO_ICING': self.images['CHOCO_ICING'],
            'CHOCO_ICING_SPRINKLES': self.images['CHOCO_ICING_SPRINKLES'],
            'LEMON_SPRINKLES': self.images['LEMON_SPRINKLES'],
            'LEMON_ICING': self.images['LEMON_ICING'],
            'LEMON_ICING_SPRINKLES': self.images['LEMON_ICING_SPRINKLES'],
            'STRAWBERRY_SPRINKLES': self.images['STRAWBERRY_SPRINKLES'],
            'STRAWBERRY_ICING': self.images['STRAWBERRY_ICING'],
            'STRAWBERRY_ICING_SPRINKLES': self.images['STRAWBERRY_ICING_SPRINKLES']
        }

        pygame.mixer.music.load(self.soundsPath + 'bgmusic.ogg')
        try:
            pygame.mixer.music.set_volume(0.5)
            pygame.mixer.music.play(-1)
        except pygame.error as e:
            print(f"Error playing background music: {e}")

        self.correctSound = pygame.mixer.Sound(self.soundsPath + 'correct.ogg')
        self.wrongSound = pygame.mixer.Sound(self.soundsPath + 'wrong.ogg')

        self.correctSound.set_volume(0.2)
        self.wrongSound.set_volume(0.2)

        self.choice = Item(self.images['CHOICE'], 180, 370)
        self.start_button = Button("START", self.black, self.lightPink, 150, 50, self.width//3-40, 500, 32)
        self.quit_button = Button("QUIT",  self.black, self.lightPink, 150, 50, (self.width//3)+160, 500, 32)
        self.controls_button = Button("CONTROLS",  self.black,  self.lightPink, 150, 50, (self.width//3)+360, 500, 32)
        self.game_over = Button("GAME OVER",  self.black, self.lightPink, 300, 100, self.width//2, self.height//2, 40)
        self.game_state = 'menu'
        self.window_open = True
        self.active_game = False

        
        self.player = Waiter({'WAITERR': self.images['WAITERR'],
                        'WAITERS1R': self.images['WAITERS1R'],
                        'WAITERS2R': self.images['WAITERS2R'],
                        'WAITERL': self.images['WAITERL'],
                        'WAITERS1L': self.images['WAITERS1L'],
                        'WAITERS2L': self.images['WAITERS2L']}, 
                        500, 
                        500, 
                        self.images,
                        self.iceCreamImages,
                        self.width,
                        self.height,
                        self.black,
                        self.correctSound,
                        self.wrongSound,
                        self.checkCollides
        )

        self.tables = [
            Table(self.images['TABLE'], 110, 120, 3000, self.player, self.images, self.iceCreamImages),
            Table(self.images['TABLE'], 500, 230, 5000, self.player, self.images, self.iceCreamImages),
            Table(self.images['TABLE'], 875, 150, 10000, self.player, self.images, self.iceCreamImages),
            Table(self.images['TABLE'], 870, 490, 15000, self.player, self.images, self.iceCreamImages)
        ]
        self.tables_group = pygame.sprite.Group(self.tables)

        self.containers = [
            Container(self.images['CONTAINER_LEMON'], 40, 510, "LEMON"),
            Container(self.images['CONTAINER_CHOCO'], 110, 510, "CHOCO"),
            Container(self.images['CONTAINER_STRAWBERRY'], 180, 510, "STRAWBERRY"),
            Container(self.images['CONTAINER_VANILLA'], 250, 510, "VANILLA"),
            Container(self.images['SPRINKLES'], 50, 250, "VANILLA_SPRINKLES"),
            Container(self.images['ICING'], 50, 385, "VANILLA_ICING"),
        ]

        self.containers_group = pygame.sprite.Group(self.containers)

        self.chairs = [
            Item(self.images['CHAIR_L'], 40, 110),
            Item(self.images['CHAIR_R'], 190, 110),
            Item(self.images['CHAIR_L'], 430, 220),
            Item(self.images['CHAIR_R'], 580, 220),
            Item(self.images['CHAIR_L'], 805, 140),
            Item(self.images['CHAIR_R'], 955, 140),
            Item(self.images['CHAIR_L'], 800, 480),
            Item(self.images['CHAIR_R'], 950, 480)
        ]   

        self.playGame()

        
    def checkCollides(self, player):
        return pygame.sprite.spritecollideany(player, self.tables_group) or pygame.sprite.spritecollideany(player, self.containers_group)

    def playGame(self):
        while self.window_open:
            self.screen.blit(self.firstBackground, (0, 0))
            self.current_time = pygame.time.get_ticks()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.window_open = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.window_open = False
                        self.active_game = False
                    elif event.key == pygame.K_q:
                        self.player.drop_ice_cream()
                    elif event.key == pygame.K_SPACE:
                        self.player.deliver_order(self.tables)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.game_state == 'menu':
                        if self.start_button.rect.collidepoint(mouse_pos):
                            self.game_state = 'game'
                            self.player.lives = 3
                            for table in self.tables:
                                table.clear_order()
                        elif self.quit_button.rect.collidepoint(mouse_pos):
                            self.window_open = False
                        elif self.controls_button.rect.collidepoint(mouse_pos):
                            self.game_state = 'controls'
                            self.controls_start_time = pygame.time.get_ticks()

            self.mouse_pos = pygame.mouse.get_pos()
            if self.game_state == 'menu':
                if self.start_button.rect.collidepoint(self.mouse_pos):
                    self.start_button.background_color = self.lightPink
                    self.start_button.text_color = self.black
                else:
                    self.start_button.background_color = self.darkPink
                    self.start_button.text_color = self.black
                if self.quit_button.rect.collidepoint(self.mouse_pos):
                    self.quit_button.background_color = self.lightPink
                    self.quit_button.text_color = self.black
                else:
                    self.quit_button.background_color = self.darkPink
                    self.quit_button.text_color = self.black
                if self.controls_button.rect.collidepoint(self.mouse_pos):
                    self.controls_button.background_color = self.lightPink
                    self.controls_button.text_color = self.black
                else:
                    self.controls_button.background_color = self.darkPink
                    self.controls_button.text_color = self.black
                self.screen.blit(self.secondBackground, (0, 0))
                self.start_button.draw(self.screen)
                self.quit_button.draw(self.screen)
                self.controls_button.draw(self.screen)

            elif self.game_state == 'game':
                self.active_game = True
                for container in self.containers:
                    if container.rect.collidepoint(self.mouse_pos):
                        container.enlarge()
                    else:
                        container.shrink()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_pos = pygame.mouse.get_pos()
                    if self.player.is_in_selection_area(self.choice):
                        for container in self.containers:
                            if container.rect.collidepoint(self.mouse_pos):
                                self.player.pick_ice_cream(self.iceCreamImages[container.flavor], container.flavor)

                for table in self.tables:
                    table.update()
                    table.draw(self.screen)
                for chair in self.chairs:
                    chair.draw(self.screen)
                for container in self.containers:
                    container.draw(self.screen)
                self.choice.draw(self.screen)

                self.player.draw(self.screen)
                self.player.update(pygame.key.get_pressed(), self.tables)
                if not self.player.lives:
                    self.game_state = 'game_over'
                    self.game_over_start_time = pygame.time.get_ticks()

            elif self.game_state == 'game_over':
                if pygame.time.get_ticks() - self.game_over_start_time < 5000:
                    self.game_over.draw(self.screen)
                else:
                    self.window_open=False

            elif self.game_state == 'controls':
                if pygame.time.get_ticks() - self.controls_start_time < 5000:
                    controls_text = Button("Controls: ", self.black, self.lightPink, 750, 50, self.width//2, self.height//2-150, 40)
                    controls_text2 = Button("Drop ice cream -> Q", self.black, self.lightPink, 750, 50, self.width // 2, self.height // 2-100, 40)
                    controls_text3 = Button("Deliver order -> Space", self.black, self.lightPink, 750, 50, self.width // 2, self.height // 2 - 50, 40)
                    controls_text4 = Button("Choose ice cream -> Leftclick", self.black, self.lightPink, 750, 50, self.width // 2, self.height // 2 , 40)
                    controls_text.draw(self.screen)
                    controls_text2.draw(self.screen)
                    controls_text3.draw(self.screen)
                    controls_text4.draw(self.screen)
                else:
                    self.game_state = 'menu'

            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()
        