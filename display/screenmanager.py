
class ScreenManager():
    def __init__(self):
        self.stack = []
        self.routes = {}
        self.routeData = None

    def registerScreen(self, route, createScreen):
        self.routes[route] = createScreen

    def getRouteData(self):
        temp = self.routeData
        self.routeData = {}
        return temp

    def route(self, route, popPreScreen=True, data=None):
        self.routeData = data
        createScreen = self.routes.get(route)
        if createScreen is None:
            raise Exception("Invalid Route")
        if popPreScreen:
            self.back()
        self.stack.append(createScreen())

    def back(self):
        if len(self.stack) <= 1:
            return
        self.stack.pop()

    def inputs(self, events):
        self.stack[-1].inputs(events)

    def update(self):
        self.stack[-1].update()

    def render(self):
        self.stack[-1].render()
