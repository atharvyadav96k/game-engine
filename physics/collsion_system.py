from physics.colliders.collision_respose import CollisionResponse

class CollisionSystem():
    def __init__(self, game_objects, detection_margin=2, velocity_iterations=12):
        self.game_objects = game_objects
        self.idx = 0
        self.collision_response = CollisionResponse()
        self.active_collisions = set()
        self.detection_margin = detection_margin
        self.velocity_iterations = velocity_iterations

    def update(self):
        self.active_collisions.clear()
        constraints = []

        for i in range(len(self.game_objects)):
            object_a = self.game_objects[i]
            if object_a.collider == None:
                continue

            for j in range(i+1, len(self.game_objects)):
                object_b = self.game_objects[j]
                if object_b.collider == None:
                    continue

                if not self.is_colliding(object_a, object_b):
                    continue

                self.idx += 1
                self.active_collisions.add(frozenset((object_a, object_b)))

                constraints.extend(self.collision_response.prepare(object_a, object_b))

        for _ in range(self.velocity_iterations):
            for constraint in constraints:
                self.collision_response.apply_velocity(constraint)

        for constraint in constraints:
            self.collision_response.apply_position_correction(constraint)

    def is_colliding(self, object_a, object_b):
        return object_a.collider.get_rect().inflate(
            self.detection_margin, self.detection_margin
        ).colliderect(object_b.collider.get_rect())

    def are_colliding(self, object_a, object_b):
        return frozenset((object_a, object_b)) in self.active_collisions
