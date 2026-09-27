import math
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
    def __init__(self, display, id, position, size, style=defaultRectangleStyle, rotation=0.0):
        super().__init__(id, style)
        self.display = display
        self.position = position
        self.size = size
        self.rotation = rotation
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])

    def _rotated_corners(self):
        center_x = self.position[0] + self.size[0] / 2
        center_y = self.position[1] + self.size[1] / 2
        half_w = self.size[0] / 2
        half_h = self.size[1] / 2
        cos_a = math.cos(self.rotation)
        sin_a = math.sin(self.rotation)

        corners = []
        for sign_x, sign_y in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
            local_x = sign_x * half_w
            local_y = sign_y * half_h
            corners.append((
                center_x + local_x * cos_a - local_y * sin_a,
                center_y + local_x * sin_a + local_y * cos_a
            ))
        return corners

    def render(self):
        borderRadius = self.elementStyle.border_radius
        borderWidth = self.elementStyle.border_width

        if self.rotation:
            corners = self._rotated_corners()
            pygame.draw.polygon(self.display, self.elementStyle.background, corners)
            if borderWidth > 0:
                pygame.draw.polygon(self.display, self.elementStyle.border_color, corners, width=borderWidth)
            return

        pygame.draw.rect(self.display, self.elementStyle.background, self.rect, border_radius=borderRadius)
        if borderWidth > 0:
            pygame.draw.rect(self.display, self.elementStyle.border_color, self.rect, width=borderWidth, border_radius=borderRadius)
