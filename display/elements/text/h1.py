from .text import Text, defaultTextStyle
import pygame

class H1(Text):
    def __init__(self, display, id, text, position, style=defaultTextStyle):
        super().__init__(display, id, text, position, style)
        self.size = 60
        self.font = pygame.font.Font(None, self.elementStyle.font_size)