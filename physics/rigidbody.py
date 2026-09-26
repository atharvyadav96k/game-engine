
class RigidBody():
    def __init__(self, velocity, acceleration, mass=1.0, use_gravity=False):
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass
        self.use_gravity = use_gravity
        self.is_kinematic = False

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

    def get_inverse_mass(self):
        if self.is_kinematic or self.mass <= 0:
            return 0.0
        return 1.0 / self.mass

    def is_kinematic_enabled(self):
        return self.is_kinematic

    def set_kinematic(self, enabled):
        self.is_kinematic = enabled

    def is_gravity_enabled(self):
        return self.use_gravity
