import os
from PIL import Image, ImageDraw

base_path = os.path.dirname(__file__)
assets_path = os.path.join(base_path, "assets")
os.makedirs(assets_path, exist_ok=True)

def save(img, name):
    img.save(os.path.join(assets_path, name))

# 🟩 трава
def grass_block():
    img = Image.new('RGBA', (64, 64), (0,0,0,0))
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, 64, 64], fill=(80, 200, 80))
    d.rectangle([0, 0, 64, 15], fill=(60, 180, 60))

    save(img, "block_grass.png")

# 🪨 камінь
def stone_block():
    img = Image.new('RGBA', (64, 64), (0,0,0,0))
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, 64, 64], fill=(120, 120, 120))
    save(img, "block_stone.png")

# 🌫 земля
def dirt_block():
    img = Image.new('RGBA', (64, 64), (0,0,0,0))
    d = ImageDraw.Draw(img)

    d.rectangle([0, 0, 64, 64], fill=(139, 90, 43))
    save(img, "block_dirt.png")

# ☁️ хмара
def cloud():
    img = Image.new('RGBA', (256, 128), (0,0,0,0))
    d = ImageDraw.Draw(img)

    d.ellipse([20, 20, 120, 100], fill=(255,255,255,200))
    d.ellipse([80, 10, 180, 110], fill=(255,255,255,200))
    d.ellipse([140, 30, 240, 110], fill=(255,255,255,200))

    save(img, "cloud.png")

# 🌄 фон неба
def sky_background():
    img = Image.new('RGBA', (800, 600), (135, 206, 235))
    save(img, "sky.png")

grass_block()
stone_block()
dirt_block()
cloud()
sky_background()

print("✔ World assets created!")