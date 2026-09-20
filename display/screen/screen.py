
class Screen():
    def __init__(self, display):
        self.display = display
        self.children = []

    def inputs(self, event):
        pass
    
    def update(self):
        pass

    def render(self):
        for child in self.children:
            child.render()