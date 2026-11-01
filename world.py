"""Процедурна генерація блокового світу для гри на Ursina."""

from math import sin, cos
import random


# Менший радіус дає значно вищий FPS, але світ усе ще достатній для дослідження.
WORLD_SIZE = 18
WORLD_SEED = 20261101


def terrain_height(x, z):
    """Повертає плавну висоту поверхні без додаткових бібліотек."""
    waves = sin(x * 0.18) * 2.2 + cos(z * 0.16) * 1.8
    detail = sin((x + z) * 0.43) * 0.7 + cos((x - z) * 0.31) * 0.6
    return max(1, round(4 + waves + detail))


def make_tree(Block, x, ground_y, z, rng):
    """Створює дерево над уже згенерованою поверхнею."""
    trunk_height = rng.randint(3, 4)
    for y in range(ground_y + 1, ground_y + trunk_height + 1):
        Block(position=(x, y, z), block_type='wood')

    crown_y = ground_y + trunk_height
    for dx in range(-2, 3):
        for dz in range(-2, 3):
            for dy in range(-1, 2):
                if abs(dx) + abs(dz) + abs(dy) <= 3:
                    Block(position=(x + dx, crown_y + dy, z + dz), block_type='leaves')


def generate_world(Block, size=WORLD_SIZE, seed=WORLD_SEED):
    """Створює рельєф, підземні шари та дерева; повертає висоту в центрі."""
    rng = random.Random(seed)
    heights = {}

    for x in range(-size, size + 1):
        for z in range(-size, size + 1):
            surface = terrain_height(x, z)
            heights[(x, z)] = surface
            # Створюємо лише видимі шари. Глибокі блоки не видно й вони не
            # впливають на геймплей, але суттєво знижують FPS.
            for y in range(surface - 3, surface + 1):
                if y == surface:
                    block_type = 'grass'
                elif y >= surface - 2:
                    block_type = 'dirt'
                else:
                    block_type = 'stone'
                Block(position=(x, y, z), block_type=block_type)

    # Не ставимо дерево поруч із точкою появи гравця.
    for _ in range(size * 2):
        x, z = rng.randint(-size + 2, size - 2), rng.randint(-size + 2, size - 2)
        if x * x + z * z < 36 or rng.random() > 0.18:
            continue
        make_tree(Block, x, heights[(x, z)], z, rng)

    return heights[(0, 0)]
