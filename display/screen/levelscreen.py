from .screen import Screen
from display.elements.button.playbutton import PlayButton, Button
from display.elements.text.h1 import H1

class LevelScreen(Screen):
    def __init__(self, display, screenManager):
        super().__init__(display, screenManager)
        self.children.append(H1(self.display, "Screen 2", (10, 10)))
        self.children.append(PlayButton(self.display, "Click Screen 2", (10, 300), (150, 70)))
        self.children.append(Button(self.display, "Back", (10, 400), (200, 70)))