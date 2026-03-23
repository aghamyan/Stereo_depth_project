"""Core stereo-vision calculations."""

from math import inf, pi, sin


def compute_disparity(x_left: int, x_right: int) -> int:
    """Return the absolute horizontal disparity in pixels."""
    return abs(int(x_left) - int(x_right))



def compute_distance(
    x_left: float,
    x_right: float,
    image_width: float,
    field_of_view_degrees: float,
    baseline: float,
) -> float:
    """Return depth in meters using triangulation from image-space angles."""
    if x_left == x_right:
        return inf

    beta = (180 - field_of_view_degrees) / 2
    degrees_per_pixel = field_of_view_degrees / image_width

    phi = (x_left * degrees_per_pixel) + beta
    theta = (x_right * degrees_per_pixel) + beta

    phi_rad = (180 - phi) * pi / 180
    theta_rad = (180 - theta) * pi / 180

    alpha = 180 - (phi + theta)
    alpha_rad = alpha * pi / 180

    if alpha_rad == 0:
        return inf

    numerator = baseline * sin(theta_rad) * sin(phi_rad)
    denominator = sin(alpha_rad)
    if denominator == 0:
        return inf

    return numerator / denominator
