from .screen import Screen
from display.elements.button.playbutton import PlayButton, Button
from display.elements.text.h1 import H1

class LevelScreen(Screen):
    def __init__(self, display, screenManager):
        super().__init__(display, screenManager)
        self.children.append(H1(self.display, "","Screen 2", (10, 10)))
        self.children.append(PlayButton(self.display, "btn-2","Click Screen 2", (10, 300)))
        self.children.append(Button(self.display, "btn-3","Back", (10, 400)))

    def update(self):
        for child in self.children:
            if child.isTriggerd():
                event = child.getEvent()
                if event.get("id") == "btn-3":
                    self.screenManager.route("main-screen")