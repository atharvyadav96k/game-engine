from core.vector2 import Vector2
from physics.colliders.circle_collider import CircleCollider


class CollisionInfo():
    def __init__(self, normal, penetration):
        self.normal = normal
        self.penetration = penetration


def compute_aabb_manifold(rect_a, rect_b):
    overlap_x = min(rect_a.right, rect_b.right) - max(rect_a.left, rect_b.left)
    overlap_y = min(rect_a.bottom, rect_b.bottom) - max(rect_a.top, rect_b.top)

    if overlap_x <= 0 or overlap_y <= 0:
        return None

    center_a = Vector2(rect_a.centerx, rect_a.centery)
    center_b = Vector2(rect_b.centerx, rect_b.centery)
    delta = center_b - center_a

    if overlap_x < overlap_y:
        normal = Vector2(1.0 if delta.x >= 0 else -1.0, 0.0)
        penetration = overlap_x
    else:
        normal = Vector2(0.0, 1.0 if delta.y >= 0 else -1.0)
        penetration = overlap_y

    return CollisionInfo(normal, penetration)


def compute_circle_manifold(circle_a, circle_b):
    center_a = Vector2.from_tuple(circle_a.get_center())
    center_b = Vector2.from_tuple(circle_b.get_center())
    delta = center_b - center_a
    distance = delta.length()
    radius_sum = circle_a.get_radius() + circle_b.get_radius()

    if distance >= radius_sum:
        return None

    normal = delta.normalize() if distance > 0 else Vector2(0.0, -1.0)
    penetration = radius_sum - distance
    return CollisionInfo(normal, penetration)


def compute_circle_box_manifold(circle, box):
    """Normal points from box to circle."""
    center = Vector2.from_tuple(circle.get_center())
    rect = box.get_rect()

    closest = Vector2(
        max(rect.left, min(center.x, rect.right)),
        max(rect.top, min(center.y, rect.bottom))
    )

    delta = center - closest
    distance = delta.length()
    radius = circle.get_radius()

    if distance >= radius:
        return None

    normal = delta.normalize() if distance > 0 else Vector2(0.0, -1.0)
    penetration = radius - distance
    return CollisionInfo(normal, penetration)


def compute_manifold(collider_a, collider_b):
    a_is_circle = isinstance(collider_a, CircleCollider)
    b_is_circle = isinstance(collider_b, CircleCollider)

    if a_is_circle and b_is_circle:
        return compute_circle_manifold(collider_a, collider_b)

    if not a_is_circle and not b_is_circle:
        return compute_aabb_manifold(collider_a.get_rect(), collider_b.get_rect())

    if a_is_circle:
        info = compute_circle_box_manifold(collider_a, collider_b)
        flip = True
    else:
        info = compute_circle_box_manifold(collider_b, collider_a)
        flip = False

    if info is None:
        return None

    normal = info.normal.scale(-1) if flip else info.normal
    return CollisionInfo(normal, info.penetration)
