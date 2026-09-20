from .button import Button

class PlayButton(Button):
    def __init__(self, display, text, position, size):
        super().__init__(display, text, position, size)
        self.color = (0, 0, 200)
