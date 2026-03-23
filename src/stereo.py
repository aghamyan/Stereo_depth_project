"""Core stereo-vision calculations."""

from math import inf


def compute_disparity(x_left: int, x_right: int) -> int:
    """Return the absolute horizontal disparity in pixels."""
    return abs(int(x_left) - int(x_right))



def compute_distance(disparity: float, focal_length: float, baseline: float) -> float:
    """Return depth in meters using the stereo vision formula."""
    if disparity == 0:
        return inf
    return (focal_length * baseline) / disparity
