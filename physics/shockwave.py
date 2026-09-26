import pygame
from core.vector2 import Vector2
from physics.colliders.line_of_sight import is_path_blocked_by


def linear_falloff(distance, max_radius):
    return max(0.0, 1.0 - (distance / max_radius))


def inverse_square_falloff(distance, max_radius):
    if distance >= max_radius:
        return 0.0
    return 1.0 / (1.0 + (distance / (max_radius * 0.15)) ** 2)


class ShockWave():
    def __init__(self, origin, game_objects, max_radius=300.0, expansion_speed=500.0,
                 strength=800.0, falloff=linear_falloff):
        self.origin = origin
        self.game_objects = game_objects
        self.max_radius = max_radius
        self.expansion_speed = expansion_speed
        self.strength = strength
        self.falloff = falloff
        self.radius = 0.0
        self.affected_ids = set()
        self.is_finished = False

    def update(self, delta):
        if self.is_finished:
            return

        self.radius += self.expansion_speed * delta
        if self.radius >= self.max_radius:
            self.is_finished = True

        center = self._get_center(self.origin)

        for obj in self.game_objects:
            if obj is self.origin or obj.rigidbody is None or obj.id in self.affected_ids:
                continue

            target_center = self._get_center(obj)
            distance = (target_center - center).length()
            if distance > self.radius:
                continue

            self.affected_ids.add(obj.id)

            if self._is_occluded(center, target_center, obj):
                continue

            self._apply_force(obj, center, target_center, distance)

    def render(self, display, color=(255, 140, 0), width=3):
        if self.is_finished:
            return
        center = self._get_center(self.origin)
        pygame.draw.circle(display, color, (int(center.x), int(center.y)), int(self.radius), width=width)

    def _get_center(self, obj):
        if obj.collider is not None:
            return Vector2.from_tuple(obj.collider.get_center())
        position = obj.transform.position
        size = obj.transform.size
        return Vector2(position[0] + size[0] / 2, position[1] + size[1] / 2)

    def _is_occluded(self, center, target_center, target_obj):
        for obj in self.game_objects:
            if obj is target_obj or obj is self.origin or obj.collider is None:
                continue
            if is_path_blocked_by(center, target_center, obj.collider):
                return True
        return False

    def _apply_force(self, obj, center, target_center, distance):
        direction = (target_center - center).normalize()
        magnitude = self.strength * self.falloff(distance, self.max_radius)
        obj.rigidbody.add_velocity(direction.scale(magnitude).to_tuple())
