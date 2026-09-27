from objects import GameObject, Transform
from physics.rigidbody import RigidBody
from physics.colliders.circle_collider import CircleCollider
from physics.physics_material import PhysicsMaterial
from physics.shockwave import ShockWave, inverse_square_falloff
from core.vector2 import Vector2

from . import constants as c


def _spawn_projectile(display, id_gen, prefix, origin_center, direction, offset, speed, size, color):
    pos = origin_center + direction.scale(offset)
    go = GameObject(display, id_gen(prefix),
                     Transform((pos.x - size[0] / 2, pos.y - size[1] / 2), size), color)
    go.rigidbody = RigidBody(direction.scale(speed).to_tuple(), (0, 0), mass=0.05, use_gravity=False)
    go.collider = CircleCollider(go, PhysicsMaterial(restitution=0.3, friction=0.1))
    return go


class WeaponSystem:
    """Owns every in-flight bullet/bomb and the shockwaves bombs leave behind,
    and resolves their collisions/damage each frame."""

    def __init__(self, display, id_gen, game_objects):
        self.display = display
        self.id_gen = id_gen
        self.game_objects = game_objects
        self.player_bullets = []
        self.enemy_bullets = []
        self.bombs = []
        self.shockwaves = []

    def reset(self):
        self.player_bullets = []
        self.enemy_bullets = []
        self.bombs = []
        self.shockwaves = []

    def fire_player_bullet(self, origin_center, direction):
        go = _spawn_projectile(self.display, self.id_gen, "bullet", origin_center, direction,
                                30, c.BULLET_SPEED, (8, 8), (255, 230, 80))
        self.game_objects.append(go)
        self.player_bullets.append({"go": go, "ttl": c.BULLET_TTL, "dir": direction})

    def fire_enemy_bullet(self, origin_center, direction):
        go = _spawn_projectile(self.display, self.id_gen, "ebullet", origin_center, direction,
                                26, c.ENEMY_BULLET_SPEED, (8, 8), (255, 120, 60))
        self.game_objects.append(go)
        self.enemy_bullets.append({"go": go, "ttl": c.BULLET_TTL, "dir": direction})

    def throw_bomb(self, origin_center, direction):
        size = (14, 14)
        pos = origin_center + direction.scale(26)
        go = GameObject(self.display, self.id_gen("bomb"),
                         Transform((pos.x - size[0] / 2, pos.y - size[1] / 2), size),
                         (60, 140, 60))
        go.rigidbody = RigidBody(direction.scale(c.BOMB_THROW_SPEED).to_tuple(), (0, 0),
                                  mass=1.0, use_gravity=True, use_rotation=True)
        go.collider = CircleCollider(go, PhysicsMaterial(restitution=0.35, friction=0.6))
        self.game_objects.append(go)
        self.bombs.append({"go": go, "fuse": c.BOMB_FUSE})

    def _detonate_bomb(self, bomb, player, enemies):
        go = bomb["go"]
        wave = ShockWave(go, self.game_objects, max_radius=c.BOMB_RADIUS,
                          expansion_speed=900, strength=900, falloff=inverse_square_falloff)
        self.shockwaves.append(wave)

        center = Vector2.from_tuple(go.collider.get_center())

        if player.is_alive():
            dist = (player.center() - center).length()
            if dist <= c.BOMB_RADIUS:
                player.hp -= c.BOMB_MAX_DAMAGE * max(0.0, 1.0 - dist / c.BOMB_RADIUS)

        for enemy in enemies:
            if not enemy.is_alive():
                continue
            dist = (enemy.center() - center).length()
            if dist <= c.BOMB_RADIUS:
                enemy.hp -= c.BOMB_MAX_DAMAGE * max(0.0, 1.0 - dist / c.BOMB_RADIUS)

        if go in self.game_objects:
            self.game_objects.remove(go)

    def update(self, delta, collision_system, player, enemies):
        for bullet in self.player_bullets:
            bullet["ttl"] -= delta
        for bullet in self.enemy_bullets:
            bullet["ttl"] -= delta
        for bomb in self.bombs:
            bomb["fuse"] -= delta

        remaining = []
        for bullet in self.player_bullets:
            hit_enemy = None
            for enemy in enemies:
                if enemy.is_alive() and collision_system.are_colliding(bullet["go"], enemy.go):
                    hit_enemy = enemy
                    break
            expired = bullet["ttl"] <= 0
            if hit_enemy is not None:
                hit_enemy.hp -= c.GUN_DAMAGE
                hit_enemy.go.rigidbody.add_velocity(bullet["dir"].scale(c.KNOCKBACK_SPEED).to_tuple())
            if hit_enemy is not None or expired:
                if bullet["go"] in self.game_objects:
                    self.game_objects.remove(bullet["go"])
            else:
                remaining.append(bullet)
        self.player_bullets = remaining

        remaining = []
        for bullet in self.enemy_bullets:
            hit = player.is_alive() and collision_system.are_colliding(bullet["go"], player.go)
            expired = bullet["ttl"] <= 0
            if hit:
                player.hp -= c.ENEMY_BULLET_DAMAGE
                player.go.rigidbody.add_velocity(bullet["dir"].scale(c.KNOCKBACK_SPEED).to_tuple())
            if hit or expired:
                if bullet["go"] in self.game_objects:
                    self.game_objects.remove(bullet["go"])
            else:
                remaining.append(bullet)
        self.enemy_bullets = remaining

        remaining_bombs = []
        for bomb in self.bombs:
            if bomb["fuse"] <= 0:
                self._detonate_bomb(bomb, player, enemies)
            else:
                remaining_bombs.append(bomb)
        self.bombs = remaining_bombs

        for wave in self.shockwaves:
            wave.update(delta)
        self.shockwaves = [w for w in self.shockwaves if not w.is_finished]

    def render(self, display):
        for wave in self.shockwaves:
            wave.render(display)
