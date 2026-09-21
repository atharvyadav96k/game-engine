from display.screen.screen import Screen
from display.elements.text.h1 import H1
from display.elements.button.playbutton import PlayButton
from display.elements.assets.image import Image
from display.styles.style import Style
from display.styles.stylepproperties import Property

class MainScreen(Screen):
    def __init__(self, display, screenManager):
        super().__init__(display, screenManager)
        self.children.append(H1(self.display, "","Screen 1", (10, 10), Style({Property.FONT_SIZE: 80, Property.COLOR: (255, 0, 0)})))
        self.children.append(PlayButton(self.display, "btn-1","Click Screen 1", (10, 300)))
        self.children.append(Image(self.display, "image", (100, 100), (100, 100)))

    def update(self):
        for child in self.children:
            if child.isTriggerd():
                event = child.getEvent()
                if event.get("id") == "btn-1":
                    self.screenManager.route("level-screen")
