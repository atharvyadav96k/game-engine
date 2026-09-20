from display.screen.screen import Screen
from display.elements.text.h1 import H1
from display.elements.button.playbutton import PlayButton

class MainScreen(Screen):
    def __init__(self, display, screenManager):
        super().__init__(display, screenManager)
        self.children.append(H1(self.display, "Screen 1", (10, 10)))
        self.children.append(PlayButton(self.display, "Click Screen 1", (10, 300), (100, 70)))

    def update(self):
        pass