from ursina import *
from player import Player

app = Ursina()

Sky()
DirectionalLight().look_at(Vec3(1, -1, -1))
AmbientLight(color=color.white)

# 🟢 стартовий режим (меню)
mouse.locked = False
mouse.visible = True
window.cursor_visible = True


# 🎯 CROSSHAIR (+)
crosshair = Text(
    "+",
    parent=camera.ui,
    scale=2,
    origin=(0, 0),
    position=(0, 0),
    color=color.white
)
crosshair.enabled = False


# 🧍 гравець
player = Player(position=(0, 3, 0))
player.enabled = False


# 🌍 блок
class Block(Button):
    def __init__(self, position=(0, 0, 0), col=color.green):
        super().__init__(
            model='cube',
            position=position,
            color=col,
            collider='box',
            parent=scene
        )

    def input(self, key):
        if self.hovered:
            if key == 'left mouse down':
                destroy(self)

            if key == 'right mouse down':
                Block(position=self.position + mouse.normal, col=color.green)


# 🌍 світ
WORLD_SIZE = 10

for x in range(-WORLD_SIZE, WORLD_SIZE):
    for z in range(-WORLD_SIZE, WORLD_SIZE):
        Block(position=(x, 0, z))


# 🎮 МЕНЮ
menu = Entity(parent=camera.ui)

# 🌑 тінь тексту
title_shadow = Text(
    "MY GAME",
    parent=menu,
    scale=3,
    origin=(0, 0),
    position=(0.01, 0.24),
    color=color.black
)

# ✨ основний текст
title = Text(
    "MY GAME",
    parent=menu,
    scale=3,
    origin=(0, 0),
    position=(0, 0.25),
    color=color.azure
)


def start_game():
    menu.disable()
    player.enabled = True

    mouse.locked = True
    mouse.visible = False
    window.cursor_visible = False

    crosshair.enabled = True


Button(
    text="START",
    parent=menu,
    scale=(0.3, 0.1),
    y=-0.1,
    color=color.azure,
    on_click=start_game
)

app.run()