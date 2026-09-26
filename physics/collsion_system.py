from physics.colliders.collision_respose import CollisionResponse

class CollisionSystem():
    def __init__(self, game_objects):
        self.game_objects = game_objects
        self.idx = 0
        self.collision_response = CollisionResponse()

    def update(self):
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
                    self.on_collision(object_a, object_b)

    def is_colliding(self, object_a, object_b):
        return object_a.collider.get_rect().colliderect(
            object_b.collider.get_rect()
        )

    def on_collision(self, object_a, object_b):
        self.collision_response.resolve(object_a, object_b)