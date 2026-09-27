
class Transform():
    def __init__(self, position, size, rotation=0.0):
        self.position = position
        self.size = size
        self.rotation = rotation

    def move(self, x, y):
        self.position  = (self.position[0] + x, self.position[1] + y)

    def rotate(self, delta_angle):
        self.rotation += delta_angle