import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # Викликаємо конструктор класу Sprite
        self.run_images = [pygame.image.load("assets/player_run1.png").convert_alpha(),
                           pygame.image.load("assets/player_run2.png").convert_alpha()]
        self.jump_image = pygame.image.load("assets/player_jump.png").convert_alpha()
        self.index = 0
        self.image = self.run_images[self.index]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.vel_y = 0
        self.is_jumping = False
        self.gravity = 0.8

    def update(self):
        # Анімація бігу
        if not self.is_jumping:
            self.index += 0.1
            if self.index >= len(self.run_images):
                self.index = 0
            self.image = self.run_images[int(self.index)]
        else:
            self.image = self.jump_image

        # Додаємо гравітацію
        self.vel_y += self.gravity
        self.rect.y += self.vel_y

        # Перевірка на падіння
        if self.rect.bottom > 500:  # Зупиняємо падіння на землі
            self.rect.bottom = 500
            self.is_jumping = False
            self.vel_y = 0

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.vel_y = -15  # сила стрибка
