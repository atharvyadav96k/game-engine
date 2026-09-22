
class PhysicsSystem():
    def __init__(self, game_objects):
        self.game_objects = game_objects

    def update(self, delta):
        for object in self.game_objects:
            if object.rigidbody == None:
                continue

            rigidbody = object.rigidbody
            transform = object.transform

            rigidbody.velocity = (
                rigidbody.velocity[0] + rigidbody.acceleration[0] * delta,
                rigidbody.velocity[1] + rigidbody.acceleration[1] * delta
            )

            transform.position = (
                transform.position[0] + rigidbody.velocity[0] * delta,
                transform.position[1] + rigidbody.velocity[1] * delta
            )