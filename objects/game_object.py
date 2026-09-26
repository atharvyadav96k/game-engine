from display.elements.rectangle import Rectangle
from display.elements.circle import Circle
from display.styles.style import Style
from display.styles.stylepproperties import Property
from physics.colliders.circle_collider import CircleCollider

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
        style = Style({
            Property.BACKGROUND: self.color,
        })

        if isinstance(self.collider, CircleCollider):
            self.rect = Circle(self.display, "", self.collider.get_center(), self.collider.get_radius(), style)
        else:
            self.rect = Rectangle(self.display, "", self.transform.position, self.transform.size, style)

        self.rect.render()
