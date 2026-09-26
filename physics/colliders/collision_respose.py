from core.vector2 import Vector2
from physics.colliders.collision_math import compute_manifold
from physics.physics_material import PhysicsMaterial


class CollisionResponse():
    def __init__(self, percent_correction=0.8, slop=0.01, rest_velocity_threshold=50.0):
        self.percent_correction = percent_correction
        self.slop = slop
        self.rest_velocity_threshold = rest_velocity_threshold

    def resolve(self, object_a, object_b):
        collider_a = object_a.collider
        collider_b = object_b.collider

        if not collider_a.is_physics_response_enabled() or not collider_b.is_physics_response_enabled():
            return

        info = compute_manifold(collider_a, collider_b)
        if info is None:
            return

        rigidbody_a = object_a.rigidbody
        rigidbody_b = object_b.rigidbody
        inv_mass_a = rigidbody_a.get_inverse_mass() if rigidbody_a is not None else 0.0
        inv_mass_b = rigidbody_b.get_inverse_mass() if rigidbody_b is not None else 0.0
        total_inv_mass = inv_mass_a + inv_mass_b

        if total_inv_mass == 0:
            return

        normal = info.normal

        self._apply_positional_correction(object_a, object_b, normal, info.penetration, inv_mass_a, inv_mass_b, total_inv_mass)

        material = PhysicsMaterial.combine(collider_a.material, collider_b.material)

        velocity_a = Vector2.from_tuple(rigidbody_a.velocity) if rigidbody_a is not None else Vector2(0, 0)
        velocity_b = Vector2.from_tuple(rigidbody_b.velocity) if rigidbody_b is not None else Vector2(0, 0)
        relative_velocity = velocity_b - velocity_a
        velocity_along_normal = relative_velocity.dot(normal)

        if velocity_along_normal > 0:
            return

        is_resting_contact = abs(velocity_along_normal) < self.rest_velocity_threshold
        restitution = 0.0 if is_resting_contact else material.restitution
        impulse_scalar = -(1 + restitution) * velocity_along_normal / total_inv_mass
        impulse = normal.scale(impulse_scalar)

        if rigidbody_a is not None and inv_mass_a > 0:
            rigidbody_a.velocity = (velocity_a - impulse.scale(inv_mass_a)).to_tuple()
        if rigidbody_b is not None and inv_mass_b > 0:
            rigidbody_b.velocity = (velocity_b + impulse.scale(inv_mass_b)).to_tuple()

        self._apply_friction(object_a, object_b, normal, material, impulse_scalar, inv_mass_a, inv_mass_b, total_inv_mass)

    def _apply_positional_correction(self, object_a, object_b, normal, penetration, inv_mass_a, inv_mass_b, total_inv_mass):
        correction_magnitude = max(penetration - self.slop, 0.0) / total_inv_mass * self.percent_correction
        correction = normal.scale(correction_magnitude)

        if object_a.rigidbody is not None and inv_mass_a > 0:
            self._move(object_a, correction.scale(-inv_mass_a))
        if object_b.rigidbody is not None and inv_mass_b > 0:
            self._move(object_b, correction.scale(inv_mass_b))

    def _apply_friction(self, object_a, object_b, normal, material, impulse_scalar, inv_mass_a, inv_mass_b, total_inv_mass):
        rigidbody_a = object_a.rigidbody
        rigidbody_b = object_b.rigidbody

        velocity_a = Vector2.from_tuple(rigidbody_a.velocity) if rigidbody_a is not None else Vector2(0, 0)
        velocity_b = Vector2.from_tuple(rigidbody_b.velocity) if rigidbody_b is not None else Vector2(0, 0)
        relative_velocity = velocity_b - velocity_a

        tangent_velocity = relative_velocity - normal.scale(relative_velocity.dot(normal))
        tangent = tangent_velocity.normalize()
        if tangent.length() == 0:
            return

        velocity_along_tangent = relative_velocity.dot(tangent)
        friction_impulse_scalar = -velocity_along_tangent / total_inv_mass

        max_friction = abs(impulse_scalar) * material.friction
        friction_impulse_scalar = max(-max_friction, min(max_friction, friction_impulse_scalar))
        friction_impulse = tangent.scale(friction_impulse_scalar)

        if rigidbody_a is not None and inv_mass_a > 0:
            rigidbody_a.velocity = (velocity_a - friction_impulse.scale(inv_mass_a)).to_tuple()
        if rigidbody_b is not None and inv_mass_b > 0:
            rigidbody_b.velocity = (velocity_b + friction_impulse.scale(inv_mass_b)).to_tuple()

    def _move(self, obj, delta_vector):
        obj.transform.position = (
            obj.transform.position[0] + delta_vector.x,
            obj.transform.position[1] + delta_vector.y
        )
