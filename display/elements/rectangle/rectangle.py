import pygame
from ..element import Element
from ...styles.style import Style
from ...styles.stylepproperties import Property

defaultRectangleStyle = Style({
    Property.BACKGROUND: (255, 255, 255),
    Property.BORDER_COLOR: (0, 0, 0),
    Property.BORDER_WIDTH: 0,
    Property.BORDER_RADIUS: 0
})

class Rectangle(Element):
    def __init__(self, display, id, position, size, style=defaultRectangleStyle):
        super().__init__(id, style)
        self.display = display
        self.position = position
        self.size = size
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def render(self):
        borderRadius = self.elementStyle.border_radius
        pygame.draw.rect(self.display, self.elementStyle.background, self.rect, border_radius=borderRadius)
        borderWidth = self.elementStyle.border_width
        if borderWidth > 0:
            pygame.draw.rect(self.display, self.elementStyle.border_color, self.rect, width=borderWidth, border_radius=borderRadius)
