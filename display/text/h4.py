from .text import Text
import pygame

class H4(Text):
    def __init__(self, display, text, position):
        super().__init__(display, text, position)
        self.size = 32
        self.font = pygame.font.Font(None, self.size)