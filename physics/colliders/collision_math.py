from core.vector2 import Vector2


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
