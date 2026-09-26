from physics.colliders.collision_respose import CollisionResponse

class CollisionSystem():
    def __init__(self, game_objects, detection_margin=2):
        self.game_objects = game_objects
        self.idx = 0
        self.collision_response = CollisionResponse()
        self.active_collisions = set()
        self.detection_margin = detection_margin

    def update(self):
        self.active_collisions.clear()

        for i in range(len(self.game_objects)):
            object_a = self.game_objects[i]
            if object_a.collider == None:
                continue

            for j in range(i+1, len(self.game_objects)):
                object_b = self.game_objects[j]
                if object_b.collider == None:
                    continue

                if self.is_colliding(object_a, object_b):
                    self.idx+=1
                    self.active_collisions.add(frozenset((object_a, object_b)))
                    self.on_collision(object_a, object_b)

    def is_colliding(self, object_a, object_b):
        return object_a.collider.get_rect().inflate(
            self.detection_margin, self.detection_margin
        ).colliderect(object_b.collider.get_rect())

    def are_colliding(self, object_a, object_b):
        return frozenset((object_a, object_b)) in self.active_collisions

    def on_collision(self, object_a, object_b):
        self.collision_response.resolve(object_a, object_b)