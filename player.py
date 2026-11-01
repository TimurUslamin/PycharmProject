from ursina import *


class Player(Entity):
    """Легкий контролер від першої особи."""

    def __init__(self, position=(0, 6, 0)):
        super().__init__(position=position, collider='box', scale=(0.8, 1.8, 0.8))
        self.speed = 5
        self.jump_force = 9
        self.gravity = 20
        self.velocity_y = 0
        self.grounded = False
        self.active = False
        self.pitch = 0
        self.surface_height = None

    def enter_world(self):
        camera.parent = self
        camera.position = (0, 1.55, 0)
        # На старті камера дивиться на землю, щоб рельєф був одразу видимий.
        self.pitch = -18
        camera.rotation = (self.pitch, 0, 0)
        self.active = True

    def update(self):
        if not self.active:
            return

        self.rotation_y += mouse.velocity[0] * 100
        self.pitch = clamp(self.pitch - mouse.velocity[1] * 100, -90, 90)
        camera.rotation_x = self.pitch

        movement = Vec3(held_keys['d'] - held_keys['a'], 0, held_keys['w'] - held_keys['s'])
        direction = self.forward * movement.z + self.right * movement.x
        if direction.length() > 0:
            direction = direction.normalized()
            self.move(direction)

        # Довший промінь стабільно знаходить землю навіть за просідання FPS.
        ground = raycast(self.position + Vec3(0, 0.2, 0), Vec3(0, -1, 0),
                         distance=3.0, ignore=(self,))
        # Якщо колайдери не відповіли, використовуємо висоту процедурного
        # рельєфу. Це гарантує, що гравець не пройде крізь землю.
        floor_y = None
        if ground.hit:
            floor_y = ground.world_point.y + 0.91
        elif self.surface_height is not None:
            floor_y = self.surface_height(self.x, self.z)

        if floor_y is not None and self.y <= floor_y + 0.15 and self.velocity_y <= 0:
            self.grounded = True
            self.velocity_y = 0
            self.y = floor_y
        else:
            self.grounded = False
            self.velocity_y -= self.gravity * time.dt
            self.y += self.velocity_y * time.dt

    def move(self, direction):
        step = 0.35
        horizontal = Vec3(direction.x, 0, direction.z)
        hit = raycast(self.position + Vec3(0, 0.5, 0), horizontal,
                      distance=step, ignore=(self,))
        if not hit.hit:
            self.position += horizontal * self.speed * time.dt

    def input(self, key):
        if self.active and key == 'space' and self.grounded:
            self.velocity_y = self.jump_force
            self.grounded = False
