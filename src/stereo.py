"""Core stereo-vision calculations."""

from math import inf, radians, tan


def compute_disparity(x_left: int, x_right: int) -> int:
    """Return the absolute horizontal disparity in pixels."""
    return abs(int(x_left) - int(x_right))


def compute_focal_length_pixels(image_width: float, field_of_view_degrees: float) -> float:
    """Convert horizontal FOV into focal length expressed in pixels."""
    if image_width <= 0:
        raise ValueError("image_width must be positive")
    if field_of_view_degrees <= 0 or field_of_view_degrees >= 180:
        raise ValueError("field_of_view_degrees must be in (0, 180)")

    return image_width / (2 * tan(radians(field_of_view_degrees) / 2))


def compute_distance(
    x_left: float,
    x_right: float,
    image_width: float,
    field_of_view_degrees: float,
    baseline: float,
) -> float:
    """Return depth in meters using the classic stereo equation Z = (f * B) / d."""
    if baseline <= 0:
        raise ValueError("baseline must be positive")

    disparity = compute_disparity(x_left, x_right)
    if disparity == 0:
        return inf

    focal_length_pixels = compute_focal_length_pixels(image_width, field_of_view_degrees)
    return (focal_length_pixels * baseline) / disparity
