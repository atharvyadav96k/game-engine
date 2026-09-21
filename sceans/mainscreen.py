from display.screen.screen import Screen
from display.elements.text.h1 import H1
from display.elements.button.playbutton import PlayButton
from display.elements.assets.image import Image
from display.styles.style import Style
from display.styles.stylepproperties import Property, TextAlign
from enum import Enum

class styling(Enum):
    headingStyle = Style({
        Property.FONT_SIZE: 80, 
        Property.COLOR: (255, 0, 0)
    })

    playButton = Style({
        Property.BORDER_COLOR: (255, 0, 0),
        Property.COLOR: (0, 0, 0),
        Property.BACKGROUND: (255, 255, 255),
        Property.BORDER_RADIUS: 5,
    })

class MainScreen(Screen):
    def __init__(self, display, screenManager):
        super().__init__(display, screenManager)
        self.children.append(H1(self.display, "","Screen 1", (10, 10), styling.headingStyle.value))
        self.children.append(PlayButton(self.display, "btn-1","Click Screen 1", (10, 300)))
        self.children.append(Image(self.display, "image", (100, 100), (100, 100)))

    def update(self):
        for child in self.children:
            if child.isTriggerd():
                event = child.getEvent()
                if event.get("id") == "btn-1":
                    self.screenManager.route("level-screen")
