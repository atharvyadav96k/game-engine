from .stylepproperties import Property, TextAlign

DEFAULTS = {
    Property.BACKGROUND: (255, 255, 255),
    Property.BORDER_COLOR: (0, 0, 0),
    Property.BORDER_WIDTH: 0,
    Property.BORDER_RADIUS: 0,

    Property.COLOR: (255, 255, 255),
    Property.FONT: None,
    Property.FONT_SIZE: 20,
    Property.TEXT_ALIGN_VERTICAL: TextAlign.ALIGN_CENTER,
    Property.TEXT_ALIGN_HORINZANTAL: TextAlign.ALIGN_CENTER,

    Property.OPACITY: 1,
    Property.ROTATION: 0,
    Property.SCALE: 1,

    Property.MARGIN_VERTICAL: 0,
    Property.MARGIN_HORIZANTAL: 0,
    Property.PADDING_VERTICAL: 0,
    Property.PADDING_HORIZANTAL: 0,
}

class Style:
    def __init__(self, style):
        self.background = style.get(Property.BACKGROUND, DEFAULTS[Property.BACKGROUND])
        self.border_color = style.get(Property.BORDER_COLOR, DEFAULTS[Property.BORDER_COLOR])
        self.border_width = style.get(Property.BORDER_WIDTH, DEFAULTS[Property.BORDER_WIDTH])
        self.border_radius = style.get(Property.BORDER_RADIUS, DEFAULTS[Property.BORDER_RADIUS])

        self.color = style.get(Property.COLOR, DEFAULTS[Property.COLOR])
        self.font = style.get(Property.FONT, DEFAULTS[Property.FONT])
        self.font_size = style.get(Property.FONT_SIZE, DEFAULTS[Property.FONT_SIZE])
        self.text_align_vertical = style.get(Property.TEXT_ALIGN_VERTICAL, DEFAULTS[Property.TEXT_ALIGN_VERTICAL])
        self.text_align_horizantal = style.get(Property.TEXT_ALIGN_HORINZANTAL, DEFAULTS[Property.TEXT_ALIGN_HORINZANTAL])

        self.opacity = style.get(Property.OPACITY, DEFAULTS[Property.OPACITY])
        self.rotation = style.get(Property.ROTATION, DEFAULTS[Property.ROTATION])
        self.scale = style.get(Property.SCALE, DEFAULTS[Property.SCALE])

        self.padding_vertical = style.get(Property.PADDING_VERTICAL, DEFAULTS[Property.PADDING_VERTICAL])
        self.padding_horizantal = style.get(Property.PADDING_HORIZANTAL, DEFAULTS[Property.PADDING_HORIZANTAL])