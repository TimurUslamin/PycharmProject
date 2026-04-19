import pygame
import os

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()

        base_path = os.path.dirname(__file__)
        image_path = os.path.join(base_path, "assets", "platform.png")

        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (width, height))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)