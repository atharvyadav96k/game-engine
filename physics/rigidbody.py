
class RigidBody():
    def __init__(self, velocity, acceleration, mass=1.0, use_gravity=False,
                 angular_velocity=0.0, torque=0.0, moment_of_inertia=None, use_rotation=False):
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass
        self.use_gravity = use_gravity
        self.is_kinematic = False

        self.angular_velocity = angular_velocity
        self.torque = torque
        self.use_rotation = use_rotation
        self.moment_of_inertia = moment_of_inertia

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

    def set_angular_velocity(self, angular_velocity):
        self.angular_velocity = angular_velocity

    def add_angular_velocity(self, angular_velocity):
        self.angular_velocity += angular_velocity

    def set_torque(self, torque):
        self.torque = torque

    def add_torque(self, torque):
        self.torque += torque

    def set_moment_of_inertia(self, moment_of_inertia):
        self.moment_of_inertia = moment_of_inertia

    def get_inverse_inertia(self):
        if not self.use_rotation or self.is_kinematic:
            return 0.0
        if self.moment_of_inertia is None or self.moment_of_inertia <= 0:
            return 0.0
        return 1.0 / self.moment_of_inertia

    def is_rotation_enabled(self):
        return self.use_rotation

    def set_rotation_enabled(self, enabled):
        self.use_rotation = enabled
