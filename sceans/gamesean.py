from display.screen.screen import Screen
from display.elements.button.button import Button
from objects import GameObject, Transform
from physics.rigidbody import RigidBody
from physics.physics_system import PhysicsSystem
from physics.collsion_system import CollisionSystem
from physics.colliders.collider import Collider
from physics.physics_material import PhysicsMaterial
from time import time
import pygame

class GameSean(Screen):
    def __init__(self, display, screenManager):
        super().__init__(display, screenManager)
        self.game_sean()
        self.game_objects = self.game_object()
        self.collisionSystem = CollisionSystem(self.game_objects)
        self.physics = PhysicsSystem(self.game_objects, gravity=(0, 980.0))
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
                (0, 0),
                (0, 0),
                mass=1.0,
                use_gravity=True
        )
        self.ground1 = GameObject(self.display, "player-2", Transform(
                (100, 200),
                (500, 10)
            )
        )
        self.ground2 = GameObject(self.display, "player-3", Transform(
             (400, 400),
             (500, 10)
        ))
        self.player1.collider = Collider(self.player1, PhysicsMaterial(restitution=0.7, friction=0.3))
        self.ground1.collider = Collider(self.ground1, PhysicsMaterial(restitution=0.0, friction=0.8))
        self.ground2.collider = Collider(self.ground2, PhysicsMaterial(restitution=0.0, friction=0.2))
        return [self.player1, self.ground1, self.ground2]

    def inputs(self, events):
        speed = 400
        super().inputs(events)
        for event in events:
             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.collisionSystem.are_colliding(self.ground2, self.player1):
                    self.player1.rigidbody.add_velocity((0, -400))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_d]:
            self.player1.transform.move(speed*self.delta, 0)
        if keys[pygame.K_a]:
            self.player1.transform.move(-speed*self.delta, 0) 

    def update(self):
        self.currt_time = time()
        self.delta = self.currt_time - self.prev_time
        for child in self.children:
            if child.isTriggerd():
                event = child.getEvent()
                if event.get("id") == "pause":
                    self.screenManager.route("level-screen")

        self.physics.update(self.delta)
        self.collisionSystem.update()
        self.prev_time = self.currt_time

    def render(self):
        for objects in self.game_objects:
                    objects.render()

        super().render()
