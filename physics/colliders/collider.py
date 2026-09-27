
import pygame
from core.vector2 import Vector2
from physics.physics_material import PhysicsMaterial

class Collider():
    def __init__(self, game_object, material=None):
        self.game_object = game_object
        self.material = material if material is not None else PhysicsMaterial()
        self.enable_physics_response = True

    def get_rotation(self):
        return self.game_object.transform.rotation

    def get_half_extents(self):
        width, height = self.game_object.transform.size
        return (width / 2.0, height / 2.0)

    def get_axes(self):
        rotation = self.get_rotation()
        return (Vector2(1.0, 0.0).rotate(rotation), Vector2(0.0, 1.0).rotate(rotation))

    def get_center_vector(self):
        position = self.game_object.transform.position
        size = self.game_object.transform.size
        return Vector2(position[0] + size[0] / 2.0, position[1] + size[1] / 2.0)

    def get_corners(self):
        center = self.get_center_vector()
        half_w, half_h = self.get_half_extents()
        axis_x, axis_y = self.get_axes()

        corners = []
        for sign_x, sign_y in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            corners.append(center + axis_x.scale(sign_x * half_w) + axis_y.scale(sign_y * half_h))
        return corners

    def get_rect(self):
        if self.get_rotation() == 0:
            return pygame.Rect(
                self.game_object.transform.position,
                self.game_object.transform.size
            )

        corners = self.get_corners()
        xs = [corner.x for corner in corners]
        ys = [corner.y for corner in corners]
        left, top = min(xs), min(ys)
        return pygame.Rect(left, top, max(xs) - left, max(ys) - top)

    def get_center(self):
        center = self.get_center_vector()
        return (center.x, center.y)

    def get_moment_of_inertia(self, mass):
        width, height = self.game_object.transform.size
        return (mass / 12.0) * (width ** 2 + height ** 2)

    def is_physics_response_enabled(self):
        return self.enable_physics_response

    def set_physics_response_enabled(self, enabled):
        self.enable_physics_response = enabled
