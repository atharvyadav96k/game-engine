from .text import Text
import pygame

class H5(Text):
    def __init__(self, display, id, text, position):
        super().__init__(display, id, text, position)
        self.size = 24
        self.font = pygame.font.Font(None, self.size)