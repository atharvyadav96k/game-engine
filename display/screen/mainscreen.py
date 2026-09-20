from display.screen.screen import Screen
from display.text.h1 import H1
from display.button.playbutton import PlayButton

class MainScreen(Screen):
    def __init__(self, display, screenManager):
        super().__init__(display, screenManager)
        self.buttons = [PlayButton(self.display, "Click Screen 1", (10, 300), (100, 70))]
        self.children.append(H1(self.display, "Screen 1", (10, 10)))
        self.children.extend(self.buttons)

    def inputs(self, events):
        for button in self.buttons:
            if button.inputs(events) == True:
                self.screenManager.route("level-screen")

    def update(self):
        pass