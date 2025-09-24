from PIL import Image, ImageDraw

# Створення простого спрайту гравця (біг)
def create_player_run_sprite():
    width, height = 50, 80
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, height], fill=(0, 0, 255, 255))  # синій прямокутник
    img.save('assets/player_run1.png')

    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, height], fill=(0, 0, 255, 255))  # синій прямокутник
    img.save('assets/player_run2.png')

# Створення простого спрайту гравця (стрибок)
def create_player_jump_sprite():
    width, height = 50, 80
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, height], fill=(255, 0, 0, 255))  # червоний прямокутник
    img.save('assets/player_jump.png')

# Створення платформи
def create_platform_sprite():
    width, height = 200, 20
    img = Image.new('RGBA', (width, height), (255, 255, 255, 0))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, height], fill=(0, 255, 0, 255))  # зелена платформа
    img.save('assets/platform.png')

# Створення фону
def create_background_sprite():
    width, height = 800, 600
    img = Image.new('RGBA', (width, height), (135, 206, 235, 255))  # блакитне небо
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 500, width, height], fill=(0, 128, 0, 255))  # зелена земля
    img.save('assets/background.png')

from PIL import Image, ImageDraw

def create_background():
    width, height = 800, 600  # Розміри фону
    img = Image.new('RGBA', (width, height), (135, 206, 235, 255))  # Блакитне небо
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 500, width, height], fill=(0, 128, 0, 255))  # Зелена земля
    img.save('assets/background.png')  # Збереження у папку assets

create_background()
print("Фон згенерований і збережений!")


# Генерація всіх спрайтів
create_player_run_sprite()
create_player_jump_sprite()
create_platform_sprite()
create_background_sprite()

print("Спрайти згенеровані!")
