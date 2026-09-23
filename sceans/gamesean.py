from display.screen.screen import Screen
from display.elements.button.button import Button
from objects import GameObject, Transform
from physics.rigidbody import RigidBody
from physics.physics_system import PhysicsSystem
from physics.collsion_system import CollisionSystem
from physics.colliders.collider import Collider
from time import time

class GameSean(Screen):
    def __init__(self, display, screenManager):
        super().__init__(display, screenManager)
        self.game_sean()
        self.game_objects = self.game_object()
        self.collisionSystem = CollisionSystem(self.game_objects)
        self.physics = PhysicsSystem(self.game_objects)
        self.prev_time = time()
        self.currt_time = time()

    def game_sean(self):
        self.children.append(Button(self.display, "pause", "II", (10, 10)))

    def game_object(self):
        self.player1 = GameObject(self.display ,"player-1", Transform(
                    (300, 100),
                    (20, 20)
                ))
        self.player1.rigidbody = RigidBody(
                (0, 20),
                (0, 0)
        )
        self.player2 = GameObject(self.display, "player-2", Transform(
                (100, 200),
                (500, 10)
            )
        )
        self.player3 = GameObject(self.display, "player-3", Transform(
             (100, 300),
             (500, 10)
        ))
        self.player2.collider = Collider(self.player2)
        self.player1.collider = Collider(self.player1)
        self.player3.collider = Collider(self.player3)
        return [self.player1, self.player2, self.player3]

    def update(self):
        self.currt_time = time()
        delta = self.currt_time - self.prev_time
        for child in self.children:
            if child.isTriggerd():
                event = child.getEvent()
                if event.get("id") == "pause":
                    self.screenManager.route("level-screen")

        self.physics.update(delta)
        self.collisionSystem.update()
        self.prev_time = self.currt_time

    def render(self):
        for objects in self.game_objects:
                    objects.render()

        super().render()
