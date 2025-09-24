import pygame
from player import Player
from platform import Platform

# Ініціалізація Pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Паркур Гра")

clock = pygame.time.Clock()
FPS = 60

# Фонове зображення
background = pygame.image.load("assets/background.png").convert()

# Створення групи спрайтів для гравця і платформ
player_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()

# Створюємо об'єкт гравця і додаємо його до групи
player = Player(100, 400)
player_group.add(player)

# Створюємо платформу і додаємо її до групи
ground = Platform(0, 500, WIDTH, 100)
platform_group.add(ground)

running = True
while running:
    clock.tick(FPS)

    # Обробка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # Оновлення групи спрайтів
    player_group.update()

    # Перевірка на зіткнення гравця з платформою
    hits = pygame.sprite.spritecollide(player, platform_group, False)
    if hits:
        if player.vel_y > 0:  # Якщо гравець падає
            player.rect.bottom = hits[0].rect.top
            player.vel_y = 0
            player.is_jumping = False

    # Малюємо на екрані
    screen.blit(background, (0, 0))  # Малюємо фон
    platform_group.draw(screen)  # Малюємо платформи
    player_group.draw(screen)  # Малюємо гравця

    pygame.display.flip()  # Оновлюємо екран

pygame.quit()
