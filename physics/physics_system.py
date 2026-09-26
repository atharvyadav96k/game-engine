
class PhysicsSystem():
    def __init__(self, game_objects, gravity=(0, 980.0)):
        self.game_objects = game_objects
        self.gravity = gravity

    def update(self, delta):
        for object in self.game_objects:
            if object.rigidbody == None:
                continue

            rigidbody = object.rigidbody
            if rigidbody.is_kinematic_enabled():
                continue

            transform = object.transform

            acceleration = rigidbody.acceleration
            if rigidbody.is_gravity_enabled():
                acceleration = (
                    acceleration[0] + self.gravity[0],
                    acceleration[1] + self.gravity[1]
                )

            rigidbody.velocity = (
                rigidbody.velocity[0] + acceleration[0] * delta,
                rigidbody.velocity[1] + acceleration[1] * delta
            )

            transform.position = (
                transform.position[0] + rigidbody.velocity[0] * delta,
                transform.position[1] + rigidbody.velocity[1] * delta
            )
