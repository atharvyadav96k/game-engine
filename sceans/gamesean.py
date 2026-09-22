from display.screen.screen import Screen
from display.elements.button.button import Button
from objects import GameObject, Transform
from physics.rigidbody import RigidBody
from physics.physics_system import PhysicsSystem
from time import time

class GameSean(Screen):
    def __init__(self, display, screenManager):
        super().__init__(display, screenManager)
        self.game_sean()
        self.game_objects = self.game_object()
        self.physics = PhysicsSystem(self.game_objects)
        self.prev_time = time()
        self.currt_time = time()

    def game_sean(self):
        self.children.append(Button(self.display, "pause", "II", (10, 10)))

    def game_object(self):
        self.player = GameObject(self.display ,"player", Transform(
                    (100, 100),
                    (20, 20)
                ))
        self.player.rigidbody = RigidBody(
                (100, 0),
                (0, 100)
        )
        return [self.player]

    def update(self):
        self.currt_time = time()
        delta = self.currt_time - self.prev_time
        for child in self.children:
            if child.isTriggerd():
                event = child.getEvent()
                if event.get("id") == "pause":
                    self.screenManager.route("level-screen")

        for objects in self.game_objects:
            objects.render()

        self.physics.update(delta)
        print(self.player.transform.position)
        self.prev_time = self.currt_time
