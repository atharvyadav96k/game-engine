from core.vector2 import Vector2
from physics.colliders.circle_collider import CircleCollider


class ContactPoint():
    def __init__(self, position, penetration):
        self.position = position
        self.penetration = penetration


class CollisionInfo():
    def __init__(self, normal, contact_points):
        self.normal = normal
        self.contact_points = contact_points


def _project(corners, axis):
    projections = [corner.dot(axis) for corner in corners]
    return min(projections), max(projections)


def _incident_edge(box, normal):
    """The box edge whose outward normal is most anti-parallel to `normal`, as (p0, p1)."""
    axis_x, axis_y = box.get_axes()
    corners = box.get_corners()
    edges = (
        (axis_y.scale(-1), corners[0], corners[1]),
        (axis_x, corners[1], corners[2]),
        (axis_y, corners[2], corners[3]),
        (axis_x.scale(-1), corners[3], corners[0]),
    )
    return min(edges, key=lambda edge: edge[0].dot(normal))[1:]


def compute_box_manifold(box_a, box_b):
    """SAT collision between two (possibly rotated) oriented boxes."""
    corners_a = box_a.get_corners()
    corners_b = box_b.get_corners()
    candidate_axes = (
        (box_a.get_axes()[0], box_a, 0),
        (box_a.get_axes()[1], box_a, 1),
        (box_b.get_axes()[0], box_b, 0),
        (box_b.get_axes()[1], box_b, 1),
    )

    min_overlap = None
    min_axis = None
    ref_box = None
    ref_axis_index = None

    for axis, owner, axis_index in candidate_axes:
        min_a, max_a = _project(corners_a, axis)
        min_b, max_b = _project(corners_b, axis)
        overlap = min(max_a, max_b) - max(min_a, min_b)

        if overlap <= 0:
            return None

        if min_overlap is None or overlap < min_overlap:
            min_overlap = overlap
            min_axis = axis
            ref_box = owner
            ref_axis_index = axis_index

    center_a = box_a.get_center_vector()
    center_b = box_b.get_center_vector()
    delta = center_b - center_a

    normal = min_axis.normalize()
    if delta.dot(normal) < 0:
        normal = normal.scale(-1)

    incident_box = box_b if ref_box is box_a else box_a
    p0, p1 = _incident_edge(incident_box, normal)

    ref_tangent = ref_box.get_axes()[1 - ref_axis_index]
    ref_tangent_half = ref_box.get_half_extents()[1 - ref_axis_index]
    ref_normal_half = ref_box.get_half_extents()[ref_axis_index]
    ref_center = ref_box.get_center_vector()

    def clip(point):
        tangent_coord = (point - ref_center).dot(ref_tangent)
        clamped = max(-ref_tangent_half, min(tangent_coord, ref_tangent_half))
        return point + ref_tangent.scale(clamped - tangent_coord)

    contact_points = []
    for point in (clip(p0), clip(p1)):
        # Clamp to min_overlap: the SAT axis test already established this is
        # the true, worst-case overlap depth for the pair. Without this clamp,
        # a near-tied incident-edge selection can occasionally pick a corner
        # far from the reference face and report a spuriously huge penetration,
        # causing a single massive (runaway) position correction.
        penetration = min(ref_normal_half - (point - ref_center).dot(normal), min_overlap)
        if penetration <= 0:
            continue
        contact_points.append(ContactPoint(point, penetration))

    if not contact_points:
        return None

    return CollisionInfo(normal, contact_points)


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
    return CollisionInfo(normal, [ContactPoint(contact_point, penetration)])


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

    return CollisionInfo(normal, [ContactPoint(closest, penetration)])


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
    return CollisionInfo(normal, info.contact_points)
