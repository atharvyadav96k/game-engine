from ..display.elements.rectangle import Rectangle
import pygame

class GameObject():
    def __init__(self, display ,id, transform):
        self.id = id
        self.transform = transform
        self.rigidbody = None
        self.display = display
        
    def update(self):
        pass

    def render(self):
        self.rect = Rectangle(self.display, "", self.transform.position, self.transform.size)
