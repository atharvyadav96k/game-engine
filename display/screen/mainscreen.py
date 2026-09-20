from display.screen.screen import Screen
from display.text.h1 import H1

class MainScreen(Screen):
    def __init__(self, display):
        super().__init__(display)
        self.welcomeMessage = H1(self.display, "Welcome", (10, 10))

    def inputs(self, event):
        pass

    def update(self):
        pass

    def render(self):
        self.welcomeMessage.render()