import os
import pygame
from ..element import Element

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "assets")

class Image(Element):
    def __init__(self, display, id, position, size, path=os.path.join(ASSETS_DIR, "placeholder.jpg")):
        super().__init__(id)
        self.display = display
        self.image = pygame.transform.scale(pygame.image.load(path).convert_alpha(), size)
        self.position =  position
        self.size = size

    def render(self):
        self.display.blit(self.image, self.position)

    