import math


class Vector2():
    def __init__(self, x=0.0, y=0.0):
        self.x = x
        self.y = y

    @staticmethod
    def from_tuple(t):
        return Vector2(t[0], t[1])

    def to_tuple(self):
        return (self.x, self.y)

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def scale(self, s):
        return Vector2(self.x * s, self.y * s)

    def dot(self, other):
        return self.x * other.x + self.y * other.y

    def length(self):
        return math.sqrt(self.dot(self))

    def normalize(self):
        length = self.length()
        if length == 0:
            return Vector2(0, 0)
        return Vector2(self.x / length, self.y / length)
