from .text import Text
import pygame

class H1(Text):
    def __init__(self, display, text, position):
        super().__init__(display, text, position)
        self.size = 60
        self.font = pygame.font.Font(None, self.size)