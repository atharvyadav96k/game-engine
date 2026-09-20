from .text import Text
import pygame

class H3(Text):
    def __init__(self, display, id, text, position):
        super().__init__(display, id, text, position)
        self.size = 42
        self.font = pygame.font.Font(None, self.size)