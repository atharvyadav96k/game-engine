import pygame
from ..element import Element
from ..text import Text

class Button(Element):
    def __init__(self, display, id,text, position, size):
        super().__init__(id)
        self.STANDERD_INPUT = True
        self.text = text
        self.position = position
        self.size = size
        self.display = display
        self.color = (100, 100, 100)
        self.rect = pygame.Rect(self.position[0], self.position[1], self.size[0], self.size[1])
        self.displayText = Text(self.display, "",text, position)

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
        pygame.draw.rect(self.display, self.color, self.rect)
        self.displayText.render()