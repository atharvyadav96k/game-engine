from .screen import Screen
from display.button.playbutton import PlayButton
from display.text.h1 import H1

class LevelScreen(Screen):
    def __init__(self, display):
        super().__init__(display)
        self.children.append(H1(self.display, "Screen 2", (10, 10)))
        self.children.append(PlayButton(self.display, "Click Screen 2", (10, 300), (150, 70)))
