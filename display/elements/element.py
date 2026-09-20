import pygame

class Element:
    def __init__(self, id):
        self.id = id
        self.STANDERD_INPUT = False
        self.isGetTriggerByEvent = False
        self.lastEvent = None

    def inputs(self, events):
        pass

    def isAcceptInput(self):
        return self.STANDERD_INPUT

    def update(self):
        pass

    def getEvent(self):
        temp = self.lastEvent
        self.lastEvent = None
        return {
            'id': self.id,
            'event': temp
        }

    def isTriggerd(self):
        return self.isGetTriggerByEvent

    def render(self):
        pass