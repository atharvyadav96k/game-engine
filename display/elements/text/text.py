import pygame
from ..element import Element

class Text(Element):
    def __init__(self, display, id, text, position):
        super().__init__(id)
        self.display = display
        self.text = text
        self.position = position
        self.size = 50
        self.font = pygame.font.Font(None, self.size)

    def render(self):
        surface = self.font.render(self.text, True, (255, 255, 255))
        self.display.blit(surface, self.position)