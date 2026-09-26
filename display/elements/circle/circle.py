import pygame
from ..element import Element
from ...styles.style import Style
from ...styles.stylepproperties import Property

defaultCircleStyle = Style({
    Property.BACKGROUND: (255, 255, 255),
    Property.BORDER_COLOR: (0, 0, 0),
    Property.BORDER_WIDTH: 0,
})

class Circle(Element):
    def __init__(self, display, id, center, radius, style=defaultCircleStyle):
        super().__init__(id, style)
        self.display = display
        self.center = center
        self.radius = radius

    def render(self):
        pygame.draw.circle(self.display, self.elementStyle.background, self.center, self.radius)
        borderWidth = self.elementStyle.border_width
        if borderWidth > 0:
            pygame.draw.circle(self.display, self.elementStyle.border_color, self.center, self.radius, width=borderWidth)
