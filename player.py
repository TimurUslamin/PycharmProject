from ursina import *

class Player(Entity):
    def __init__(self, position=(0, 3, 0)):
        super().__init__(
            model='cube',
            color=color.azure,
            scale=(0.8, 1.8, 0.8),
            position=position,
            collider='box'
        )

        # ⚙️ рух
        self.speed = 5
        self.jump_force = 6
        self.gravity = 20
        self.velocity_y = 0
        self.grounded = False

        # 🖱️ камера
        self.sensitivity = 100
        self.pitch = 0

        camera.parent = self
        camera.position = (0, 1.6, 0)

    def update(self):

        # 🖱️ поворот
        self.rotation_y += mouse.velocity[0] * self.sensitivity

        self.pitch -= mouse.velocity[1] * self.sensitivity
        self.pitch = clamp(self.pitch, -80, 80)

        camera.rotation_x = self.pitch

        # 🎮 рух
        move = Vec3(
            held_keys['d'] - held_keys['a'],
            0,
            held_keys['w'] - held_keys['s']
        )

        direction = (self.right * move.x + self.forward * move.z)
        direction.y = 0

        if direction.length() > 0:
            self.try_move(direction.normalized())

        self.apply_gravity()

    # 🧱 рух
    def try_move(self, direction):
        hit = raycast(
            self.world_position + Vec3(0, 1, 0),
            direction,
            distance=0.5,
            ignore=(self,)
        )

        if not hit.hit:
            self.position += direction * self.speed * time.dt

    # 🌍 гравітація (СТАБІЛЬНА)
    def apply_gravity(self):
        hit = raycast(
            self.world_position + Vec3(0, 0.1, 0),
            Vec3(0, -1, 0),
            distance=1.1,
            ignore=(self,)
        )

        if hit.hit:
            if self.velocity_y <= 0:
                self.grounded = True
                self.velocity_y = 0
                self.y = hit.world_point.y + 1
        else:
            self.grounded = False
            self.velocity_y -= self.gravity * time.dt
            self.y += self.velocity_y * time.dt

    # 🦘 стрибок
    def input(self, key):
        if key == 'space' and self.grounded:
            self.velocity_y = self.jump_force
            self.grounded = False