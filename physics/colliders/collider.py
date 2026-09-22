
import pygame

class Collider():
    def __init__(self, game_object):
        self.game_object = game_object

    def get_rect(self):
        return pygame.Rect(
            self.game_object.transform.position,
            self.game_object.transform.size
        )