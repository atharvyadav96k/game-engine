
class RigidBody():
    def __init__(self, velocity, acceleration, mass=1.0, use_gravity=False,
                 angular_velocity=0.0, torque=0.0, moment_of_inertia=None, use_rotation=False,
                 sleep_threshold_linear=6.0, sleep_threshold_angular=0.05, sleep_delay=0.5):
        self.velocity = velocity
        self.acceleration = acceleration
        self.mass = mass
        self.use_gravity = use_gravity
        self.is_kinematic = False

        self.angular_velocity = angular_velocity
        self.torque = torque
        self.use_rotation = use_rotation
        self.moment_of_inertia = moment_of_inertia

        self.is_sleeping = False
        self.sleep_timer = 0.0
        self.sleep_threshold_linear = sleep_threshold_linear
        self.sleep_threshold_angular = sleep_threshold_angular
        self.sleep_delay = sleep_delay

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

    def wake(self):
        self.is_sleeping = False
        self.sleep_timer = 0.0

    def is_asleep(self):
        return self.is_sleeping

    def update_sleep_state(self, delta):
        speed_sq = self.velocity[0] ** 2 + self.velocity[1] ** 2
        angular_speed = abs(self.angular_velocity) if self.use_rotation else 0.0

        if speed_sq < self.sleep_threshold_linear ** 2 and angular_speed < self.sleep_threshold_angular:
            self.sleep_timer += delta
            if self.sleep_timer >= self.sleep_delay:
                self.is_sleeping = True
                self.velocity = (0.0, 0.0)
                self.angular_velocity = 0.0
        else:
            self.sleep_timer = 0.0
