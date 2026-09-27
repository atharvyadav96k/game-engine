from core.vector2 import Vector2
from physics.colliders.collision_math import compute_manifold
from physics.physics_material import PhysicsMaterial


class ContactConstraint():
    def __init__(self, object_a, object_b, normal, penetration, r_a, r_b,
                 inv_mass_a, inv_mass_b, inv_inertia_a, inv_inertia_b, material):
        self.object_a = object_a
        self.object_b = object_b
        self.normal = normal
        self.penetration = penetration
        self.r_a = r_a
        self.r_b = r_b
        self.inv_mass_a = inv_mass_a
        self.inv_mass_b = inv_mass_b
        self.inv_inertia_a = inv_inertia_a
        self.inv_inertia_b = inv_inertia_b
        self.material = material


class CollisionResponse():
    def __init__(self, percent_correction=0.8, slop=0.01, rest_velocity_threshold=50.0):
        self.percent_correction = percent_correction
        self.slop = slop
        self.rest_velocity_threshold = rest_velocity_threshold

    def prepare(self, object_a, object_b):
        collider_a = object_a.collider
        collider_b = object_b.collider

        if not collider_a.is_physics_response_enabled() or not collider_b.is_physics_response_enabled():
            return []

        info = compute_manifold(collider_a, collider_b)
        if info is None:
            return []

        rigidbody_a = object_a.rigidbody
        rigidbody_b = object_b.rigidbody
        inv_mass_a = rigidbody_a.get_inverse_mass() if rigidbody_a is not None else 0.0
        inv_mass_b = rigidbody_b.get_inverse_mass() if rigidbody_b is not None else 0.0

        if inv_mass_a + inv_mass_b == 0:
            return []

        inv_inertia_a = rigidbody_a.get_inverse_inertia() if rigidbody_a is not None else 0.0
        inv_inertia_b = rigidbody_b.get_inverse_inertia() if rigidbody_b is not None else 0.0

        center_a = Vector2.from_tuple(collider_a.get_center())
        center_b = Vector2.from_tuple(collider_b.get_center())

        material = PhysicsMaterial.combine(collider_a.material, collider_b.material)

        # Position correction must run once per pair, not once per contact point --
        # applying it per point (e.g. twice for a 2-point box manifold) compounds
        # into a runaway feedback loop. Only the deepest point carries a nonzero
        # penetration; the rest resolve velocity/torque only.
        deepest_index = max(range(len(info.contact_points)), key=lambda i: info.contact_points[i].penetration)

        constraints = []
        for index, contact in enumerate(info.contact_points):
            r_a = contact.position - center_a
            r_b = contact.position - center_b
            penetration = contact.penetration if index == deepest_index else 0.0
            constraints.append(ContactConstraint(
                object_a, object_b, info.normal, penetration, r_a, r_b,
                inv_mass_a, inv_mass_b, inv_inertia_a, inv_inertia_b, material
            ))
        return constraints

    def apply_velocity(self, constraint):
        object_a = constraint.object_a
        object_b = constraint.object_b
        rigidbody_a = object_a.rigidbody
        rigidbody_b = object_b.rigidbody

        self._wake_if_needed(rigidbody_a, rigidbody_b)
        self._wake_if_needed(rigidbody_b, rigidbody_a)

        if self._is_inactive(rigidbody_a) and self._is_inactive(rigidbody_b):
            return

        normal = constraint.normal
        r_a = constraint.r_a
        r_b = constraint.r_b
        inv_mass_a = constraint.inv_mass_a
        inv_mass_b = constraint.inv_mass_b
        inv_inertia_a = constraint.inv_inertia_a
        inv_inertia_b = constraint.inv_inertia_b
        material = constraint.material
        total_inv_mass = inv_mass_a + inv_mass_b

        angular_velocity_a = rigidbody_a.angular_velocity if (rigidbody_a is not None and inv_inertia_a > 0) else 0.0
        angular_velocity_b = rigidbody_b.angular_velocity if (rigidbody_b is not None and inv_inertia_b > 0) else 0.0

        velocity_a = Vector2.from_tuple(rigidbody_a.velocity) if rigidbody_a is not None else Vector2(0, 0)
        velocity_b = Vector2.from_tuple(rigidbody_b.velocity) if rigidbody_b is not None else Vector2(0, 0)
        point_velocity_a = velocity_a + r_a.perpendicular().scale(angular_velocity_a)
        point_velocity_b = velocity_b + r_b.perpendicular().scale(angular_velocity_b)
        relative_velocity = point_velocity_b - point_velocity_a
        velocity_along_normal = relative_velocity.dot(normal)

        if velocity_along_normal > 0:
            return

        angular_term_a = (r_a.cross(normal) ** 2) * inv_inertia_a
        angular_term_b = (r_b.cross(normal) ** 2) * inv_inertia_b
        effective_mass = total_inv_mass + angular_term_a + angular_term_b

        is_resting_contact = abs(velocity_along_normal) < self.rest_velocity_threshold
        restitution = 0.0 if is_resting_contact else material.restitution
        impulse_scalar = -(1 + restitution) * velocity_along_normal / effective_mass
        impulse = normal.scale(impulse_scalar)

        if rigidbody_a is not None and inv_mass_a > 0:
            rigidbody_a.velocity = (velocity_a - impulse.scale(inv_mass_a)).to_tuple()
        if rigidbody_b is not None and inv_mass_b > 0:
            rigidbody_b.velocity = (velocity_b + impulse.scale(inv_mass_b)).to_tuple()

        if rigidbody_a is not None and inv_inertia_a > 0:
            rigidbody_a.angular_velocity -= inv_inertia_a * r_a.cross(impulse)
        if rigidbody_b is not None and inv_inertia_b > 0:
            rigidbody_b.angular_velocity += inv_inertia_b * r_b.cross(impulse)

        self._apply_friction(object_a, object_b, normal, material, impulse_scalar,
                              inv_mass_a, inv_mass_b, inv_inertia_a, inv_inertia_b,
                              r_a, r_b, total_inv_mass)

    def apply_position_correction(self, constraint):
        object_a = constraint.object_a
        object_b = constraint.object_b
        inv_mass_a = constraint.inv_mass_a
        inv_mass_b = constraint.inv_mass_b
        total_inv_mass = inv_mass_a + inv_mass_b

        correction_magnitude = max(constraint.penetration - self.slop, 0.0) / total_inv_mass * self.percent_correction
        correction = constraint.normal.scale(correction_magnitude)

        if object_a.rigidbody is not None and inv_mass_a > 0:
            self._move(object_a, correction.scale(-inv_mass_a))
        if object_b.rigidbody is not None and inv_mass_b > 0:
            self._move(object_b, correction.scale(inv_mass_b))

    def _apply_friction(self, object_a, object_b, normal, material, impulse_scalar,
                         inv_mass_a, inv_mass_b, inv_inertia_a, inv_inertia_b,
                         r_a, r_b, total_inv_mass):
        rigidbody_a = object_a.rigidbody
        rigidbody_b = object_b.rigidbody

        angular_velocity_a = rigidbody_a.angular_velocity if (rigidbody_a is not None and inv_inertia_a > 0) else 0.0
        angular_velocity_b = rigidbody_b.angular_velocity if (rigidbody_b is not None and inv_inertia_b > 0) else 0.0

        velocity_a = Vector2.from_tuple(rigidbody_a.velocity) if rigidbody_a is not None else Vector2(0, 0)
        velocity_b = Vector2.from_tuple(rigidbody_b.velocity) if rigidbody_b is not None else Vector2(0, 0)
        point_velocity_a = velocity_a + r_a.perpendicular().scale(angular_velocity_a)
        point_velocity_b = velocity_b + r_b.perpendicular().scale(angular_velocity_b)
        relative_velocity = point_velocity_b - point_velocity_a

        tangent_velocity = relative_velocity - normal.scale(relative_velocity.dot(normal))
        tangent = tangent_velocity.normalize()
        if tangent.length() == 0:
            return

        angular_term_a = (r_a.cross(tangent) ** 2) * inv_inertia_a
        angular_term_b = (r_b.cross(tangent) ** 2) * inv_inertia_b
        tangent_effective_mass = total_inv_mass + angular_term_a + angular_term_b

        velocity_along_tangent = relative_velocity.dot(tangent)
        friction_impulse_scalar = -velocity_along_tangent / tangent_effective_mass

        max_friction = abs(impulse_scalar) * material.friction
        friction_impulse_scalar = max(-max_friction, min(max_friction, friction_impulse_scalar))
        friction_impulse = tangent.scale(friction_impulse_scalar)

        if rigidbody_a is not None and inv_mass_a > 0:
            rigidbody_a.velocity = (velocity_a - friction_impulse.scale(inv_mass_a)).to_tuple()
        if rigidbody_b is not None and inv_mass_b > 0:
            rigidbody_b.velocity = (velocity_b + friction_impulse.scale(inv_mass_b)).to_tuple()

        if rigidbody_a is not None and inv_inertia_a > 0:
            rigidbody_a.angular_velocity -= inv_inertia_a * r_a.cross(friction_impulse)
        if rigidbody_b is not None and inv_inertia_b > 0:
            rigidbody_b.angular_velocity += inv_inertia_b * r_b.cross(friction_impulse)

    def _is_inactive(self, rigidbody):
        return rigidbody is None or rigidbody.is_kinematic_enabled() or rigidbody.is_asleep()

    def _wake_if_needed(self, target, other):
        if target is None or not target.is_asleep():
            return
        if not self._is_inactive(other):
            target.wake()

    def _move(self, obj, delta_vector):
        obj.transform.position = (
            obj.transform.position[0] + delta_vector.x,
            obj.transform.position[1] + delta_vector.y
        )
