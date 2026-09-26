
class Transform():
    def __init__(self, position, size):
        self.position = position
        self.size = size

    def move(self, x, y):
        self.position  = (self.position[0] + x, self.position[1] + y)