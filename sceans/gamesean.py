from display.screen.screen import Screen
from display.elements.button.button import Button

class GameSean(Screen):
    def __init__(self, display, screenManager):
        super().__init__(display, screenManager)
        self.children.append(Button(self.display, "pause", "II", (10, 10)))
        data = self.screenManager.getRouteData()
        print(data["level"])

    def update(self):
        for child in self.children:
            if child.isTriggerd():
                event = child.getEvent()
                if event.get("id") == "pause":
                    self.screenManager.route("level-screen")
