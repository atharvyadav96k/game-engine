
import pygame
from physics.physics_material import PhysicsMaterial

class Collider():
    def __init__(self, game_object, material=None):
        self.game_object = game_object
        self.material = material if material is not None else PhysicsMaterial()
        self.enable_physics_response = True

    def get_rect(self):
        return pygame.Rect(
            self.game_object.transform.position,
            self.game_object.transform.size
        )

    def get_center(self):
        rect = self.get_rect()
        return (rect.centerx, rect.centery)

    def is_physics_response_enabled(self):
        return self.enable_physics_response

    def set_physics_response_enabled(self, enabled):
        self.enable_physics_response = enabled
