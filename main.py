from ursina import *
from player import Player
from world import generate_world, terrain_height
import random
import time
from math import sin


app = Ursina()
window.title = 'Block World'
window.color = color.rgb(14, 29, 49)
camera.fov = 90
Sky(texture='assets/sky.png')
DirectionalLight(shadows=False).look_at(Vec3(1, -1, -1))
AmbientLight(color=color.rgba(170, 170, 170, 0.55))
# Без туману: він може повністю вибілювати сцену на деяких відеокартах.
scene.fog_density = 0

BLOCK_TEXTURES = {
    'grass': 'assets/block_grass.png',
    'dirt': 'assets/block_dirt.png',
    'stone': 'assets/block_stone.png',
}
BLOCK_COLORS = {
    'wood': color.rgb(107, 70, 39),
    'leaves': color.rgb(54, 128, 63),
}
world_blocks = set()
item_drops = set()
# Запасна невидима підлога: не дає гравцеві впасти за межі світу.
safety_floor = Entity(parent=scene, model='cube', collider='box', visible=False,
                      position=(0, -12, 0), scale=(160, 1, 160))


class Block(Entity):
    def __init__(self, position, block_type='grass'):
        textured = block_type in BLOCK_TEXTURES
        super().__init__(
            parent=scene, model='cube', position=position, collider='box',
            texture=BLOCK_TEXTURES.get(block_type, 'white_cube'),
            color=color.white if textured else BLOCK_COLORS[block_type],
        )
        self.block_type = block_type
        world_blocks.add(self)

    def on_destroy(self):
        world_blocks.discard(self)


class ItemDrop(Entity):
    """Предмет, який з'являється після ламання і підбирається гравцем."""
    def __init__(self, position, block_type):
        textured = block_type in BLOCK_TEXTURES
        super().__init__(
            parent=scene, model='cube', position=position,
            texture=BLOCK_TEXTURES.get(block_type, 'white_cube'),
            color=color.white if textured else BLOCK_COLORS[block_type],
            scale=0.28,
        )
        self.block_type = block_type
        self.base_y = position[1]
        self.created_at = time.time()
        item_drops.add(self)

    def update(self):
        self.rotation_y += 100 * time.dt
        self.y = self.base_y + sin((time.time() - self.created_at) * 3) * 0.08

    def on_destroy(self):
        item_drops.discard(self)


player = Player()
# Резервна висота землі: потрібна, якщо рушій тимчасово не бачить колайдер блока.
player.surface_height = lambda x, z: terrain_height(round(x), round(z)) + 1.41
world_ready = False
game_running = False
last_action = 0
DEFAULT_SEED = 20261101

INVENTORY_TYPES = ('grass', 'dirt', 'stone', 'wood', 'leaves')
BLOCK_NAMES = {
    'grass': 'Трава', 'dirt': 'Земля', 'stone': 'Камінь',
    'wood': 'Дерево', 'leaves': 'Листя',
}
inventory = {block_type: 0 for block_type in INVENTORY_TYPES}
selected_block = 'dirt'

# ----- UI: усі фони мають більший z, ніж текст і кнопки, тому не перекривають їх. -----
ui = Entity(parent=camera.ui)
main_view = Entity(parent=ui)
create_view = Entity(parent=ui, enabled=False)
settings_view = Entity(parent=ui, enabled=False)
help_view = Entity(parent=ui, enabled=False)

PANEL = color.rgb(10, 28, 53)
BUTTON = color.black
# На чорній кнопці блакитна підсвітка завжди добре помітна.
HOVER = color.rgb(0, 165, 255)
TEXT = color.rgb(238, 247, 255)


def panel(parent, scale=(0.72, 0.88)):
    return Entity(parent=parent, model='quad', scale=scale, z=1, color=PANEL)


def menu_button(parent, text, y, action, width=0.48):
    return Button(parent=parent, text=text, y=y, z=0,
                  scale=(width, 0.06), color=BUTTON,
                  highlight_color=HOVER, pressed_color=color.azure,
                  text_color=TEXT, on_click=action)


panel(main_view, scale=(0.72, 0.88))
# Тінь логотипу робить його читабельним на світлому небі.
Text('BLOCK WORLD', parent=main_view, y=0.315, x=0.006, z=0,
     scale=2.6, origin=(0, 0), color=color.black)
title = Text('BLOCK WORLD', parent=main_view, y=0.327, z=-0.01,
             scale=2.6, origin=(0, 0), color=HOVER)
subtitle = Text('CREATE  •  EXPLORE  •  BUILD', parent=main_view, y=0.235,
                z=-0.01, scale=1.0, origin=(0, 0), color=TEXT)


def show(view):
    main_view.enabled = view == 'main'
    create_view.enabled = view == 'create'
    settings_view.enabled = view == 'settings'
    help_view.enabled = view == 'help'


def clear_world():
    for block in tuple(world_blocks):
        destroy(block)
    world_blocks.clear()
    for item in tuple(item_drops):
        destroy(item)
    item_drops.clear()


def build_world(seed, name):
    global world_ready
    clear_world()
    ground_y = generate_world(Block, seed=seed)
    player.position = (0, ground_y + 5, 0)
    player.velocity_y = 0
    player.pitch = 0
    player.rotation_y = 0
    world_ready = True
    world_info.text = f'{name}\nseed: {seed}'
    start_game()


def start_game():
    global game_running
    if not world_ready:
        show('create')
        return
    player.enter_world()
    game_running = True
    ui.enabled = False
    world_info.enabled = True
    crosshair.enabled = True
    hotbar.enabled = True
    mouse.locked = True
    mouse.visible = False
    window.cursor_visible = False


def pause_game():
    global game_running
    game_running = False
    player.active = False
    ui.enabled = True
    show('main')
    title.text = 'ПАУЗА'
    subtitle.text = 'ГРУ ПРИЗУПИНЕНО'
    resume_button.enabled = True
    world_info.enabled = False
    crosshair.enabled = False
    hotbar.enabled = False
    mouse.locked = False
    mouse.visible = True
    window.cursor_visible = True


def open_create():
    show('create')


def create_random_world():
    """Основна швидка дія: новий світ без введення додаткових даних."""
    build_world(random.randint(100000, 999999999), 'Новий світ')


def select_existing():
    if world_ready:
        start_game()
    else:
        build_world(DEFAULT_SEED, 'Поточний світ')


def adjust_fov(amount):
    camera.fov = int(clamp(camera.fov + amount, 65, 110))
    fov_text.text = f'Поле зору: {camera.fov}'


def adjust_fog(amount):
    scene.fog_density = clamp(scene.fog_density + amount, 0.005, 0.04)
    fog_text.text = f'Туман: {scene.fog_density:.3f}'


# Головне меню
resume_button = menu_button(main_view, 'ПРОДОВЖИТИ', 0.17, start_game)
resume_button.enabled = False
menu_button(main_view, 'НОВА ГРА', 0.07, open_create)
menu_button(main_view, 'НАЛАШТУВАННЯ', -0.03, lambda: show('settings'))
menu_button(main_view, 'ДОПОМОГА', -0.13, lambda: show('help'))

# Підменю «Нова гра»
panel(create_view)
Text('НОВА ГРА', parent=create_view, y=0.25, z=0,
     scale=1.9, origin=(0, 0), color=HOVER)
Text('Обери, що хочеш зробити', parent=create_view, y=0.16, z=0,
     scale=0.85, origin=(0, 0), color=color.light_gray)
menu_button(create_view, 'СТВОРИТИ СВІТ', 0.05, create_random_world)
menu_button(create_view, 'СТАРІ СВІТИ', -0.05, select_existing)
menu_button(create_view, 'НАЗАД', -0.18, lambda: show('main'))

# Налаштування
panel(settings_view)
Text('НАЛАШТУВАННЯ', parent=settings_view, y=0.26, z=0,
     scale=1.7, origin=(0, 0), color=HOVER)
fov_text = Text(f'Поле зору: {camera.fov}', parent=settings_view, y=0.1,
                z=0, scale=1.05, origin=(0, 0), color=TEXT)
menu_button(settings_view, 'ЗМЕНШИТИ FOV', 0.01, lambda: adjust_fov(-5))
menu_button(settings_view, 'ЗБІЛЬШИТИ FOV', -0.08, lambda: adjust_fov(5))
fog_text = Text(f'Туман: {scene.fog_density:.3f}', parent=settings_view, y=-0.18,
                z=0, scale=1.05, origin=(0, 0), color=TEXT)
menu_button(settings_view, 'МЕНШЕ ТУМАНУ', -0.27, lambda: adjust_fog(-0.005))
menu_button(settings_view, 'НАЗАД', -0.37, lambda: show('main'))

# Допомога
panel(help_view)
Text('ДОПОМОГА', parent=help_view, y=0.27, z=0, scale=1.8,
     origin=(0, 0), color=HOVER)
Text('W A S D — рух\nSPACE — стрибок\nЛКМ — зламати блок\nПКМ — поставити блок\nESC — пауза',
     parent=help_view, y=0.03, z=0, scale=1.08, origin=(0, 0), align='center', color=TEXT)
menu_button(help_view, 'НАЗАД', -0.30, lambda: show('main'))

crosshair = Text('+', parent=camera.ui, scale=2, origin=(0, 0), color=color.white, enabled=False)
world_info = Text('', parent=camera.ui, x=-0.86, y=0.46, scale=1.05,
                  color=color.white, enabled=False)

# Нижня панель інвентарю. Вона не є дочірньою меню, тому видна лише у грі.
hotbar = Entity(parent=camera.ui, y=-0.42, enabled=False)
hotbar_slots = {}
for index, block_type in enumerate(INVENTORY_TYPES):
    x = (index - 2) * 0.105
    slot = Entity(parent=hotbar, model='quad', x=x, scale=(0.095, 0.095),
                  color=color.rgb(25, 25, 25))
    icon = Entity(parent=slot, model='quad', scale=0.68,
                  texture=BLOCK_TEXTURES.get(block_type, 'white_cube'),
                  color=color.white if block_type in BLOCK_TEXTURES else BLOCK_COLORS[block_type])
    number = Text(str(index + 1), parent=slot, x=-0.4, y=0.28, scale=0.8, color=color.light_gray)
    count = Text('0', parent=slot, x=0.28, y=-0.3, scale=1.05, color=color.white)
    hotbar_slots[block_type] = (slot, count)


def refresh_hotbar():
    for block_type, (slot, count) in hotbar_slots.items():
        slot.color = HOVER if block_type == selected_block else color.rgb(25, 25, 25)
        count.text = str(inventory[block_type])


def collect_item(item):
    inventory[item.block_type] += 1
    destroy(item)
    refresh_hotbar()


refresh_hotbar()


def input(key):
    global last_action, selected_block
    if key == 'escape' and game_running:
        pause_game()
        return
    if not game_running:
        return
    if key in ('1', '2', '3', '4', '5'):
        selected_block = INVENTORY_TYPES[int(key) - 1]
        refresh_hotbar()
        return
    if key not in ('left mouse down', 'right mouse down'):
        return
    if time.time() - last_action < 0.2:
        return

    hit = raycast(camera.world_position, camera.forward, distance=5, ignore=(player,))
    if not hit.hit or not isinstance(hit.entity, Block):
        return
    last_action = time.time()
    if key == 'left mouse down':
        ItemDrop(hit.entity.position, hit.entity.block_type)
        destroy(hit.entity)
    elif inventory[selected_block] > 0:
        place = hit.entity.position + hit.normal
        Block(position=(round(place.x), round(place.y), round(place.z)), block_type=selected_block)
        inventory[selected_block] -= 1
        refresh_hotbar()


def update():
    """Підбирає предмети, коли гравець підходить до них."""
    if not game_running:
        return
    for item in tuple(item_drops):
        if distance(player.position, item.position) < 1.4:
            collect_item(item)


app.run()
