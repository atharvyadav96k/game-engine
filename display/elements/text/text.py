import pygame
from ..element import Element
from ...styles.style import Style
from ...styles.stylepproperties import Property

defaultTextStyle = Style({
    Property.FONT_SIZE : 50,
    Property.COLOR: (255, 255, 255)
})

class Text(Element):
    def __init__(self, display, id, text, position, style=defaultTextStyle):
        super().__init__(id, style)
        self.display = display
        self.text = text
        self.position = position
        self.font = pygame.font.Font(None, self.elementStyle.font_size)

    def getSize(self):
        return self.font.size(self.text)

    def render(self):
        surface = self.font.render(self.text, True, self.elementStyle.color)
        self.display.blit(surface, self.position)