from display.screen.screen import Screen
from display.text.h1 import H1
from display.button.playbutton import PlayButton

class MainScreen(Screen):
    def __init__(self, display):
        super().__init__(display)
        self.children.append(H1(self.display, "Screen 1", (10, 10)))
        self.children.append(PlayButton(self.display, "Click Screen 1", (10, 300), (100, 70)))

    def inputs(self, event):
        pass

    def update(self):
        pass