from core.vector2 import Vector2
from physics.colliders.circle_collider import CircleCollider


class CollisionInfo():
    def __init__(self, normal, penetration, contact_point):
        self.normal = normal
        self.penetration = penetration
        self.contact_point = contact_point


def _project(corners, axis):
    projections = [corner.dot(axis) for corner in corners]
    return min(projections), max(projections)


def compute_box_manifold(box_a, box_b):
    """SAT collision between two (possibly rotated) oriented boxes."""
    corners_a = box_a.get_corners()
    corners_b = box_b.get_corners()
    axes = box_a.get_axes() + box_b.get_axes()

    min_overlap = None
    min_axis = None

    for axis in axes:
        min_a, max_a = _project(corners_a, axis)
        min_b, max_b = _project(corners_b, axis)
        overlap = min(max_a, max_b) - max(min_a, min_b)

        if overlap <= 0:
            return None

        if min_overlap is None or overlap < min_overlap:
            min_overlap = overlap
            min_axis = axis

    center_a = box_a.get_center_vector()
    center_b = box_b.get_center_vector()
    delta = center_b - center_a

    normal = min_axis.normalize()
    if delta.dot(normal) < 0:
        normal = normal.scale(-1)

    contact_point = min(corners_b, key=lambda corner: corner.dot(normal))
    contact_point_a = max(corners_a, key=lambda corner: corner.dot(normal))
    if contact_point_a.dot(normal) < contact_point.dot(normal):
        contact_point = contact_point_a

    return CollisionInfo(normal, min_overlap, contact_point)


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
    contact_point = center_a + normal.scale(circle_a.get_radius())
    return CollisionInfo(normal, penetration, contact_point)


def compute_circle_box_manifold(circle, box):
    """Normal points from box to circle. Box may be rotated."""
    center = Vector2.from_tuple(circle.get_center())
    box_center = box.get_center_vector()
    axis_x, axis_y = box.get_axes()
    half_w, half_h = box.get_half_extents()

    local = center - box_center
    local_x = local.dot(axis_x)
    local_y = local.dot(axis_y)

    clamped_x = max(-half_w, min(local_x, half_w))
    clamped_y = max(-half_h, min(local_y, half_h))

    closest = box_center + axis_x.scale(clamped_x) + axis_y.scale(clamped_y)

    delta = center - closest
    distance = delta.length()
    radius = circle.get_radius()

    if distance > 0:
        if distance >= radius:
            return None
        normal = delta.normalize()
        penetration = radius - distance
    else:
        penetration_x = half_w - abs(local_x)
        penetration_y = half_h - abs(local_y)
        if penetration_x < penetration_y:
            normal = axis_x.scale(1.0 if local_x >= 0 else -1.0)
            penetration = penetration_x + radius
        else:
            normal = axis_y.scale(1.0 if local_y >= 0 else -1.0)
            penetration = penetration_y + radius

    return CollisionInfo(normal, penetration, closest)


def compute_manifold(collider_a, collider_b):
    a_is_circle = isinstance(collider_a, CircleCollider)
    b_is_circle = isinstance(collider_b, CircleCollider)

    if a_is_circle and b_is_circle:
        return compute_circle_manifold(collider_a, collider_b)

    if not a_is_circle and not b_is_circle:
        return compute_box_manifold(collider_a, collider_b)

    if a_is_circle:
        info = compute_circle_box_manifold(collider_a, collider_b)
        flip = True
    else:
        info = compute_circle_box_manifold(collider_b, collider_a)
        flip = False

    if info is None:
        return None

    normal = info.normal.scale(-1) if flip else info.normal
    return CollisionInfo(normal, info.penetration, info.contact_point)
