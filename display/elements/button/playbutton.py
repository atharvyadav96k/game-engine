from .button import Button, defaultButtonStyle

class PlayButton(Button):
    def __init__(self, display, id, text, position, style=defaultButtonStyle):
        super().__init__(display, id, text, position, style)
