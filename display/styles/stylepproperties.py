from enum import Enum

class Property(Enum):
    BACKGROUND = "background"
    COLOR = "color"
    FONT = "font"
    FONT_SIZE = "font_size"
    TEXT_ALIGN_VERTICAL = "text_align_vertical"
    TEXT_ALIGN_HORINZANTAL = "text_align_horizantal"

    BORDER_COLOR = "border_color"
    BORDER_WIDTH = "border_width"
    BORDER_RADIUS = "border_radius"

    OPACITY = "opacity"
    ROTATION = "rotation"
    SCALE = "scale"

    MARGIN_VERTICAL = "margin_vertical"
    MARGIN_HORIZANTAL = "margin_horizantal"
    PADDING_VERTICAL = "padding_vertical"
    PADDING_HORIZANTAL = "padding_horizantal"

class TextAlign(Enum):
    ALIGN_CENTER = "center"
    ALIGN_LEFT = "left"
    ALIGN_RIGHT = "right"