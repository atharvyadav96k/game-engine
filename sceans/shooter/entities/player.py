import pygame

from objects import GameObject, Transform
from physics.rigidbody import RigidBody
from physics.colliders.collider import Collider
from physics.physics_material import PhysicsMaterial
from core.vector2 import Vector2

from .. import constants as c


class Player:
    def __init__(self, display, spawn, id_gen):
        self.go = GameObject(display, id_gen("player"), Transform(spawn, c.PLAYER_SIZE), (60, 120, 220))
        self.go.rigidbody = RigidBody((0, 0), (0, 0), mass=8.0, use_gravity=True)
        self.go.collider = Collider(self.go, PhysicsMaterial(restitution=0.05, friction=0.3))

        self.hp = c.PLAYER_MAX_HP
        self.fuel = c.FUEL_MAX
        self.ammo = c.GUN_AMMO_MAX
        self.bomb_count = c.BOMB_MAX
        self.gun_timer = 0.0
        self.bomb_timer = 0.0
        self.facing = 1
        self.grounded = False

    def is_alive(self):
        return self.hp > 0

    def center(self):
        return Vector2.from_tuple(self.go.collider.get_center())

    def aim_dir(self, mouse_pos):
        direction = Vector2(mouse_pos[0], mouse_pos[1]) - self.center()
        if direction.length() == 0:
            return Vector2(self.facing, 0)
        return direction.normalize()

    def update_ground_state(self, platforms):
        rect = self.go.collider.get_rect()
        probe = pygame.Rect(rect.x, rect.bottom, rect.width, 6)
        self.grounded = any(probe.colliderect(p.collider.get_rect()) for p in platforms)

    def handle_movement(self, keys, delta):
        # a resting rigidbody falls asleep and stops being simulated entirely
        # (see RigidBody.update_sleep_state) - keep it awake while under player control
        self.go.rigidbody.wake()

        vx = 0
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            vx = -c.MOVE_SPEED
            self.facing = -1
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            vx = c.MOVE_SPEED
            self.facing = 1

        cur_vy = self.go.rigidbody.velocity[1]
        self.go.rigidbody.set_velocity((vx, cur_vy))

        jetpack_held = (keys[pygame.K_w] or keys[pygame.K_UP]) and self.fuel > 0
        if jetpack_held:
            self.go.rigidbody.set_acceleration((0, -c.JETPACK_ACCEL))
            self.fuel = max(0.0, self.fuel - c.FUEL_DRAIN * delta)
        else:
            self.go.rigidbody.set_acceleration((0, 0))
            if self.grounded:
                self.fuel = min(c.FUEL_MAX, self.fuel + c.FUEL_REGEN * delta)

    def clamp_velocity(self):
        vx, vy = self.go.rigidbody.velocity
        if vy < -c.MAX_ASCENT_SPEED:
            self.go.rigidbody.set_velocity((vx, -c.MAX_ASCENT_SPEED))

    def tick_cooldowns(self, delta):
        self.gun_timer = max(0.0, self.gun_timer - delta)
        self.bomb_timer = max(0.0, self.bomb_timer - delta)

    def can_fire_gun(self):
        return self.gun_timer <= 0 and self.ammo > 0

    def can_throw_bomb(self):
        return self.bomb_timer <= 0 and self.bomb_count > 0

    def register_gun_fire(self):
        self.ammo -= 1
        self.gun_timer = c.GUN_COOLDOWN

    def register_bomb_throw(self):
        self.bomb_count -= 1
        self.bomb_timer = c.BOMB_COOLDOWN
