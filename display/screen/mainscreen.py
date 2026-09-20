from display.screen.screen import Screen
from display.text.h1 import H1
from display.text.h2 import H2
from display.text.h3 import H3
from display.text.h4 import H4
from display.text.h5 import H5
from display.button.playbutton import PlayButton

class MainScreen(Screen):
    def __init__(self, display):
        super().__init__(display)
        self.children.append(H1(self.display, "H1", (10, 10)))
        self.children.append(H2(self.display, "H2", (10, 50)))
        self.children.append(H3(self.display, "H3", (10, 100)))
        self.children.append(H4(self.display, "H4", (10, 150)))
        self.children.append(H5(self.display, "H5", (10, 200)))
        self.children.append(PlayButton(self.display, "Click", (10, 300), (100, 70)))

    def inputs(self, event):
        pass

    def update(self):
        pass