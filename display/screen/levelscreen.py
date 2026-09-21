from .screen import Screen
from display.elements.button.playbutton import PlayButton, Button
from display.elements.text.h1 import H1

class LevelScreen(Screen):
    def __init__(self, display, screenManager):
        super().__init__(display, screenManager)
        self.count = 0
        self.children.append(H1(self.display, "","Screen 2", (10, 10)))
        self.children.append(Button(self.display, "btn-2","Click", (10, 300)))
        self.children.append(Button(self.display, "btn-3","Back", (10, 400)))
        self.countText = H1(self.display, "", str(self.count), (10, 50))
        self.children.append(self.countText)

    def update(self):
        for child in self.children:
            if child.isTriggerd():
                event = child.getEvent()
                if event.get("id") == "btn-3":
                    self.screenManager.route("main-screen")
                if event.get("id") == "btn-2":
                    self.count += 1
                    self.countText.text = str(self.count)
                    print(self.count)