import os
from PIL import Image, ImageDraw

base_path = os.path.dirname(__file__)
assets_path = os.path.join(base_path, "assets")
os.makedirs(assets_path, exist_ok=True)

def save(img, name):
    img.save(os.path.join(assets_path, name))

# 🧍 idle
def create_idle():
    img = Image.new('RGBA', (64, 128), (0,0,0,0))
    d = ImageDraw.Draw(img)

    # тіло
    d.rectangle([18, 20, 46, 90], fill=(0, 120, 255))
    # голова
    d.rectangle([20, 0, 44, 20], fill=(255, 220, 180))

    save(img, "player_idle.png")

# 🚶 ходьба 1
def create_walk1():
    img = Image.new('RGBA', (64, 128), (0,0,0,0))
    d = ImageDraw.Draw(img)

    d.rectangle([18, 20, 46, 90], fill=(0, 150, 255))
    d.rectangle([20, 0, 44, 20], fill=(255, 220, 180))

    # нога
    d.rectangle([18, 90, 30, 120], fill=(0,0,0))

    save(img, "player_walk1.png")

# 🚶 ходьба 2
def create_walk2():
    img = Image.new('RGBA', (64, 128), (0,0,0,0))
    d = ImageDraw.Draw(img)

    d.rectangle([18, 20, 46, 90], fill=(0, 150, 255))
    d.rectangle([20, 0, 44, 20], fill=(255, 220, 180))

    # інша нога
    d.rectangle([34, 90, 46, 120], fill=(0,0,0))

    save(img, "player_walk2.png")

# 🦘 jump
def create_jump():
    img = Image.new('RGBA', (64, 128), (0,0,0,0))
    d = ImageDraw.Draw(img)

    d.rectangle([18, 20, 46, 90], fill=(255, 80, 80))
    d.rectangle([20, 0, 44, 20], fill=(255, 220, 180))

    save(img, "player_jump.png")

create_idle()
create_walk1()
create_walk2()
create_jump()

print("✔ Спрайти створені!")