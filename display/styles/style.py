from .stylepproperties import Property

class Style:
    def __init__(self, style):
        self.background = style.get(Property.BACKGROUND)
        self.border_color = style.get(Property.BORDER_COLOR)
        self.border_width = style.get(Property.BORDER_WIDTH)
        self.border_radius = style.get(Property.BORDER_RADIUS)

        self.color = style.get(Property.COLOR)
        self.font = style.get(Property.FONT)
        self.font_size = style.get(Property.FONT_SIZE)

        self.opacity = style.get(Property.OPACITY)
        self.rotation = style.get(Property.ROTATION)
        self.scale = style.get(Property.SCALE)