
class PhysicsSystem():
    def __init__(self, game_objects, delta):
        self.game_objects = game_objects
        self.delta = delta

    def update(self):
        for object in self.game_objects:
            if object.rigidbody == None:
                continue

            rigidbody = object.rigidbody
            transform = object.transform

            rigidbody.velocity = (
                rigidbody.velocity[0] + rigidbody.acceleration[0] * self.delta,
                rigidbody.velocity[1] + rigidbody.acceleration[1] * self.delta
            )

            transform.position = (
                transform.position[0] + rigidbody.velocity[0] * self.delta,
                transform.position[1] + rigidbody.velocity[1] * self.delta
            )