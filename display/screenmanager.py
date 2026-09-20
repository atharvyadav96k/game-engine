
class ScreenManager():
    def __init__(self):
        self.stack = []

    def show(self, screen):
        self.stack.append(screen)

    def back(self):
        self.stack.pop()

    def inputs(self, events):
        self.stack[-1].inputs(events)

    def update(self):
        self.stack[-1].update()

    def render(self):
        self.stack[-1].render()
