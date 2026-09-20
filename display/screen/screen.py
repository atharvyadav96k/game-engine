
class Screen():
    def __init__(self, display, screenManager):
        self.display = display
        self.children = []
        self.screenManager = screenManager

    def inputs(self, event):
        pass
    
    def update(self):
        pass

    def render(self):
        for child in self.children:
            child.render()