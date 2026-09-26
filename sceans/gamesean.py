from display.screen.screen import Screen
from display.elements.button.button import Button
from objects import GameObject, Transform
from physics.rigidbody import RigidBody
from physics.physics_system import PhysicsSystem
from physics.collsion_system import CollisionSystem
from physics.colliders.collider import Collider
from physics.colliders.circle_collider import CircleCollider
from physics.physics_material import PhysicsMaterial
from physics.shockwave import ShockWave, linear_falloff, inverse_square_falloff
from time import time
import pygame

class GameSean(Screen):
    def __init__(self, display, screenManager):
        super().__init__(display, screenManager)
        self.game_sean()
        self.game_objects = self.game_object()
        self.collisionSystem = CollisionSystem(self.game_objects)
        self.physics = PhysicsSystem(self.game_objects, gravity=(0, 980.0))
        self.shockwaves = []
        self.prev_time = time()
        self.currt_time = time()

    def game_sean(self):
        self.children.append(Button(self.display, "pause", "II", (10, 10)))

    def game_object(self):
        square_left = 100
        square_top = 100
        square_right = 600
        square_bottom = 600
        wall_thickness = 20
        wall_material = PhysicsMaterial(restitution=0.3, friction=0.5)

        self.player1 = GameObject(self.display ,"player-1", Transform(
                    (300, 150),
                    (20, 20)
                ))
        self.player1.rigidbody = RigidBody(
                (0, 0),
                (0, 0),
                mass=1.0,
                use_gravity=True
        )
        self.wall_top = GameObject(self.display, "wall-top", Transform(
                (square_left - wall_thickness, square_top - wall_thickness),
                (square_right - square_left + wall_thickness * 2, wall_thickness)
            )
        )
        self.wall_bottom = GameObject(self.display, "wall-bottom", Transform(
                (square_left - wall_thickness, square_bottom),
                (square_right - square_left + wall_thickness * 2, wall_thickness)
            )
        )
        self.wall_left = GameObject(self.display, "wall-left", Transform(
                (square_left - wall_thickness, square_top - wall_thickness),
                (wall_thickness, square_bottom - square_top + wall_thickness * 2)
            )
        )
        self.wall_right = GameObject(self.display, "wall-right", Transform(
                (square_right, square_top - wall_thickness),
                (wall_thickness, square_bottom - square_top + wall_thickness * 2)
            )
        )
        self.boll1 = GameObject(self.display, "boll-1", Transform(
            (150, 550),
            (20, 20)),
            (255, 255, 255)
        )
        self.boll1.rigidbody = RigidBody(
            (50, 0),
            (0, 0),
        )
        self.boll2 = GameObject(self.display, "boll-2", Transform(
            (450, 550),
            (20, 20)),
            (0, 255, 0)
        )
        self.boll2.rigidbody = RigidBody(
             (-50, 0),
             (0, 0),
        )

        self.player1.collider = Collider(self.player1, PhysicsMaterial(restitution=0.2, friction=0.2))
        self.wall_top.collider = Collider(self.wall_top, wall_material)
        self.wall_bottom.collider = Collider(self.wall_bottom, wall_material)
        self.wall_left.collider = Collider(self.wall_left, wall_material)
        self.wall_right.collider = Collider(self.wall_right, wall_material)
        self.boll1.collider = CircleCollider(self.boll1, PhysicsMaterial(restitution=0.7, friction=0))
        self.boll2.collider = CircleCollider(self.boll2, PhysicsMaterial(restitution=0.7, friction=0))

        return [
            self.player1,
            self.wall_top, self.wall_bottom, self.wall_left, self.wall_right,
            self.boll1, self.boll2
        ]

    def trigger_shockwave(self, origin, max_radius=300.0, expansion_speed=500.0, strength=800.0,
                          falloff=linear_falloff):
        wave = ShockWave(origin, self.game_objects, max_radius, expansion_speed, strength, falloff)
        self.shockwaves.append(wave)
        return wave

    def inputs(self, events):
        speed = 400
        super().inputs(events)
        for event in events:
             if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player1.rigidbody.add_velocity((0, -400))
                if event.key == pygame.K_RETURN:
                    self.trigger_shockwave(self.player1, falloff=inverse_square_falloff)

        keys = pygame.key.get_pressed()
        current_y_velocity = self.player1.rigidbody.velocity[1]
        if keys[pygame.K_d]:
            self.player1.rigidbody.set_velocity((speed, current_y_velocity))
        elif keys[pygame.K_a]:
            self.player1.rigidbody.set_velocity((-speed, current_y_velocity))
        else:
            self.player1.rigidbody.set_velocity((0, current_y_velocity))

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

        for wave in self.shockwaves:
            wave.update(self.delta)
        self.shockwaves = [wave for wave in self.shockwaves if not wave.is_finished]

        self.prev_time = self.currt_time

    def render(self):
        for objects in self.game_objects:
                    objects.render()

        for wave in self.shockwaves:
            wave.render(self.display)

        super().render()
