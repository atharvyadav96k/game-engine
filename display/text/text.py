import pygame

class Text:
    def __init__(self, display, text, position):
        self.display = display
        self.text = text
        self.position = position
        self.size = 50
        self.font = pygame.font.Font(None, self.size)

    def render(self):
        surface = self.font.render(self.text, True, (255, 255, 255))
        self.display.blit(surface, self.position)