import pygame
from ..element import Element
from ..text import Text
from ...styles.style import Style
from ...styles.stylepproperties import Property, TextAlign

defaultButtonStyle = Style({
    Property.FONT_SIZE : 20,
    Property.COLOR: (26, 26, 26),
    Property.BACKGROUND : (255, 255, 255),
    Property.BORDER_COLOR: (168, 168, 168),
    Property.BORDER_WIDTH: 2,
    Property.PADDING_HORIZANTAL: 10,
    Property.PADDING_VERTICAL: 10,
    Property.TEXT_ALIGN_HORINZANTAL: TextAlign.ALIGN_CENTER,
    Property.TEXT_ALIGN_VERTICAL: TextAlign.ALIGN_CENTER,
    Property.BORDER_RADIUS: 0
})

class Button(Element):
    def __init__(self, display, id,text, position, style=defaultButtonStyle):
        super().__init__(id, style)
        self.STANDERD_INPUT = True
        self.text = text
        self.position = position
        self.display = display
        self.displayText = Text(self.display, "",text, position, Style({
            Property.FONT_SIZE: self.elementStyle.font_size,
            Property.COLOR: self.elementStyle.color
        }))
        text_width, text_height = self.displayText.getSize()
        self.size = (text_width + (self.elementStyle.padding_horizantal * 2), text_height + (self.elementStyle.padding_vertical * 2))
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self._alignTextPosition(text_width, text_height)

    def _alignTextPosition(self, text_width, text_height):
        horizontal_align = self.elementStyle.text_align_horizantal
        vertical_align = self.elementStyle.text_align_vertical

        if horizontal_align == TextAlign.ALIGN_LEFT:
            x = self.rect.x + self.elementStyle.padding_horizantal
        elif horizontal_align == TextAlign.ALIGN_RIGHT:
            x = self.rect.x + self.rect.width - text_width - self.elementStyle.padding_horizantal
        else:
            x = self.rect.x + (self.rect.width - text_width) / 2

        if vertical_align == TextAlign.ALIGN_LEFT:
            y = self.rect.y + self.elementStyle.padding_vertical
        elif vertical_align == TextAlign.ALIGN_RIGHT:
            y = self.rect.y + self.rect.height - text_height - self.elementStyle.padding_vertical
        else:
            y = self.rect.y + (self.rect.height - text_height) / 2

        self.displayText.position = (x, y)

    def inputs(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x = event.pos[0]
                    y = event.pos[1]
                    if x > self.position[0] and x < self.position[0] + self.size[0] and y > self.position[0] and y < self.position[1] + self.size[1]:
                        self.isGetTriggerByEvent = True
                        self.lastEvent = event     

    def update(self):
        pass

    def render(self):
        borderRadius = self.elementStyle.border_radius or 0
        pygame.draw.rect(self.display, self.elementStyle.background, self.rect, border_radius=borderRadius)
        borderWidth = self.elementStyle.border_width or 0
        if borderWidth > 0:
            pygame.draw.rect(self.display, self.elementStyle.border_color, self.rect, width=borderWidth, border_radius=borderRadius)
        self.displayText.render()