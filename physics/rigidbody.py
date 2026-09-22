
class RigidBody():
    def __init__(self, velocity, acceleration):
        self.velocity = velocity
        self.acceleration = acceleration

    def set_velocity(self, velocity):
        self.velocity = velocity

    def set_acceleration(self, acceleration):
        self.acceleration = acceleration

    def add_velocity(self, velocity):
        self.velocity = (
            velocity[0] + self.velocity[0],
            velocity[1] + self.velocity[1]
        )

    def add_acceleration(self, acceleration):
        self.acceleration = (
            acceleration[0] + self.acceleration[0],
            acceleration[1] + self.acceleration[1]
        )