import pygame

class Element:
    def __init__(self, display, text, position, size):
        self.STANDERD_INPUT = False

    def inputs(self, events):
        pass

    def isAcceptInput(self):
        return self.STANDERD_INPUT

    def update(self):
        pass

    def render(self):
        pass