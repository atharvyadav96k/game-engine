from display.elements.rectangle import Rectangle
from display.elements.circle import Circle
from display.styles.style import Style
from display.styles.stylepproperties import Property
from physics.colliders.circle_collider import CircleCollider

class GameObject():
    def __init__(self, display ,id, transform, color=(255, 0, 0)):
        self.id = id
        self.transform = transform
        self._rigidbody = None
        self.display = display
        self._collider = None
        self.color = color

    @property
    def rigidbody(self):
        return self._rigidbody

    @rigidbody.setter
    def rigidbody(self, rigidbody):
        self._rigidbody = rigidbody
        self._sync_moment_of_inertia()

    @property
    def collider(self):
        return self._collider

    @collider.setter
    def collider(self, collider):
        self._collider = collider
        self._sync_moment_of_inertia()

    def _sync_moment_of_inertia(self):
        if self._collider is None or self._rigidbody is None:
            return
        if not self._rigidbody.is_rotation_enabled():
            return
        if self._rigidbody.moment_of_inertia is not None:
            return
        self._rigidbody.set_moment_of_inertia(self._collider.get_moment_of_inertia(self._rigidbody.mass))

    def update(self):
        pass

    def render(self):
        style = Style({
            Property.BACKGROUND: self.color,
        })

        if isinstance(self.collider, CircleCollider):
            self.rect = Circle(self.display, "", self.collider.get_center(), self.collider.get_radius(), style)
        else:
            self.rect = Rectangle(self.display, "", self.transform.position, self.transform.size, style, rotation=self.transform.rotation)

        self.rect.render()
