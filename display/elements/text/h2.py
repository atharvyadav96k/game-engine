from .text import Text
import pygame

class H2(Text):
    def __init__(self, display, text, position):
        super().__init__(display, text, position)
        self.size = 52
        self.font = pygame.font.Font(None, self.size)