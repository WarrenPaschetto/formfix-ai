import math


def calculate_angle(point_a, point_b, point_c):
    """
    Calculate the angle at point_b using three points.

    Example:
    hip -> knee -> ankle

    point_a = hip
    point_b = knee
    point_c = ankle

    Returns the angle in degrees.
    """

    ax, ay = point_a
    bx, by = point_b
    cx, cy = point_c

    vector_ba = (ax - bx, ay - by)
    vector_bc = (cx - bx, cy - by)

    dot_product = vector_ba[0] * vector_bc[0] + vector_ba[1] * vector_bc[1]

    magnitude_ba = math.sqrt(vector_ba[0] ** 2 + vector_ba[1] ** 2)
    magnitude_bc = math.sqrt(vector_bc[0] ** 2 + vector_bc[1] ** 2)

    if magnitude_ba == 0 or magnitude_bc == 0:
        return 0.0

    cosine_angle = dot_product / (magnitude_ba * magnitude_bc)

    # Prevent tiny floating point errors from breaking acos.
    cosine_angle = max(-1.0, min(1.0, cosine_angle))

    angle_radians = math.acos(cosine_angle)
    angle_degrees = math.degrees(angle_radians)

    return angle_degrees