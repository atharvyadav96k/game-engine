import pygame
from physics.physics_material import PhysicsMaterial

class CircleCollider():
    def __init__(self, game_object, material=None):
        self.game_object = game_object
        self.material = material if material is not None else PhysicsMaterial()
        self.enable_physics_response = True

    def get_rect(self):
        return pygame.Rect(
            self.game_object.transform.position,
            self.game_object.transform.size
        )

    def get_radius(self):
        return self.game_object.transform.size[0] / 2

    def get_center(self):
        position = self.game_object.transform.position
        size = self.game_object.transform.size
        return (position[0] + size[0] / 2, position[1] + size[1] / 2)

    def is_physics_response_enabled(self):
        return self.enable_physics_response

    def set_physics_response_enabled(self, enabled):
        self.enable_physics_response = enabled
