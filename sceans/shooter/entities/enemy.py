from objects import GameObject, Transform
from physics.rigidbody import RigidBody
from physics.colliders.collider import Collider
from physics.physics_material import PhysicsMaterial
from physics.colliders.line_of_sight import is_path_blocked_by
from core.vector2 import Vector2

from .. import constants as c


class Enemy:
    def __init__(self, display, spawn, id_gen):
        self.go = GameObject(display, id_gen("enemy"), Transform(spawn, c.ENEMY_SIZE), (200, 60, 60))
        self.go.rigidbody = RigidBody((0, 0), (0, 0), mass=6.0, use_gravity=True)
        self.go.collider = Collider(self.go, PhysicsMaterial(restitution=0.05, friction=0.4))

        self.spawn_x = spawn[0]
        self.hp = c.ENEMY_MAX_HP
        self.direction = 1
        self.shoot_timer = c.ENEMY_SHOOT_COOLDOWN * 0.5

    def is_alive(self):
        return self.hp > 0

    def center(self):
        return Vector2.from_tuple(self.go.collider.get_center())

    def patrol(self):
        rb = self.go.rigidbody
        rb.wake()  # a resting rigidbody stops being simulated - never let a patrolling enemy sleep

        x = self.go.transform.position[0]
        if x - self.spawn_x > c.ENEMY_PATROL_RANGE:
            self.direction = -1
        elif self.spawn_x - x > c.ENEMY_PATROL_RANGE:
            self.direction = 1
        rb.set_velocity((c.ENEMY_PATROL_SPEED * self.direction, rb.velocity[1]))

    def try_get_shot_direction(self, player, platforms, delta):
        """Advances the shoot cooldown and returns a firing direction (Vector2)
        if this enemy should shoot the player this frame, else None."""
        self.shoot_timer = max(0.0, self.shoot_timer - delta)
        if not player.is_alive() or self.shoot_timer > 0:
            return None

        enemy_center = self.center()
        player_center = player.center()
        to_player = player_center - enemy_center
        if to_player.length() > c.ENEMY_SHOOT_RANGE:
            return None

        for wall in platforms:
            if is_path_blocked_by(enemy_center, player_center, wall.collider):
                return None

        self.shoot_timer = c.ENEMY_SHOOT_COOLDOWN
        return to_player.normalize()
