from display.elements.rectangle import Rectangle
from display.styles.style import Style
from display.styles.stylepproperties import Property

class GameObject():
    def __init__(self, display ,id, transform, color=(255, 0, 0)):
        self.id = id
        self.transform = transform
        self.rigidbody = None
        self.display = display
        self.collider = None
        self.color = color
        
    def update(self):
        pass

    def render(self):
        self.rect = Rectangle(self.display, "", self.transform.position, self.transform.size, Style({
            Property.BACKGROUND: self.color,
        }))
        self.rect.render()
