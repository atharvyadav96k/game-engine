
class Screen():
    def __init__(self, display, screenManager):
        self.display = display
        self.children = []
        self.screenManager = screenManager

    def inputs(self, events):
        for child in self.children:
            if child.isAcceptInput():
                child.inputs(events)
    
    def update(self):
        pass

    def render(self):
        for child in self.children:
            child.render()