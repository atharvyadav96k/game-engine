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
        self.text_align_vertical = style.get(Property.TEXT_ALIGN_VERTICAL)
        self.text_align_horizantal = style.get(Property.TEXT_ALIGN_HORINZANTAL)

        self.opacity = style.get(Property.OPACITY)
        self.rotation = style.get(Property.ROTATION)
        self.scale = style.get(Property.SCALE)

        self.padding_vertical = style.get(Property.PADDING_VERTICAL)
        self.padding_horizantal = style.get(Property.PADDING_HORIZANTAL)