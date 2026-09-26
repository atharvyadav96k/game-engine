from core.vector2 import Vector2
from physics.colliders.circle_collider import CircleCollider


def closest_point_on_segment(p1, p2, point):
    segment = p2 - p1
    segment_length_sq = segment.dot(segment)
    if segment_length_sq == 0:
        return p1

    t = (point - p1).dot(segment) / segment_length_sq
    t = max(0.0, min(1.0, t))
    return p1 + segment.scale(t)


def segment_intersects_circle(p1, p2, center, radius):
    closest = closest_point_on_segment(p1, p2, center)
    return (closest - center).length() <= radius


def segment_intersects_rect(p1, p2, rect):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    t_min, t_max = 0.0, 1.0

    for p, q in (
        (-dx, p1.x - rect.left),
        (dx, rect.right - p1.x),
        (-dy, p1.y - rect.top),
        (dy, rect.bottom - p1.y),
    ):
        if p == 0:
            if q < 0:
                return False
            continue

        t = q / p
        if p < 0:
            if t > t_max:
                return False
            t_min = max(t_min, t)
        else:
            if t < t_min:
                return False
            t_max = min(t_max, t)

    return True


def is_path_blocked_by(p1, p2, collider):
    if isinstance(collider, CircleCollider):
        center = Vector2.from_tuple(collider.get_center())
        return segment_intersects_circle(p1, p2, center, collider.get_radius())
    return segment_intersects_rect(p1, p2, collider.get_rect())
