"""Core stereo-vision calculations."""

from __future__ import annotations

from math import inf, pi, sin

import numpy as np

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

def _to_grayscale(image: np.ndarray) -> np.ndarray:
    """Convert a BGR or grayscale image to float grayscale for SSD matching."""
    if image.ndim == 2:
        return image.astype(np.float32)
    if image.ndim != 3 or image.shape[2] < 3:
        raise ValueError("Expected a grayscale or BGR image array.")

    blue = image[..., 0].astype(np.float32)
    green = image[..., 1].astype(np.float32)
    red = image[..., 2].astype(np.float32)
    return (0.114 * blue) + (0.587 * green) + (0.299 * red)

def find_match(
    left_img: np.ndarray,
    right_img: np.ndarray,
    x: int,
    y: int,
    window_size: int = 5,
    search_range: int = 100,
) -> tuple[int | None, float | None]:
    """Find the best matching x-position in the right image using SSD on the same row."""
    if window_size < 1:
        raise ValueError("window_size must be at least 1")
    if search_range < 1:
        raise ValueError("search_range must be at least 1")

    left_gray = _to_grayscale(left_img)
    right_gray = _to_grayscale(right_img)

    image_height, image_width = left_gray.shape
    right_height, right_width = right_gray.shape

    if y - window_size < 0 or y + window_size >= image_height:
        return None, None
    if y - window_size < 0 or y + window_size >= right_height:
        return None, None
    if x - window_size < 0 or x + window_size >= image_width:
        return None, None

    left_patch = left_gray[
        y - window_size : y + window_size + 1,
        x - window_size : x + window_size + 1,
    ]

    start_x = max(window_size, x - search_range)
    end_x = min(right_width - window_size - 1, x + search_range)

    if start_x > end_x:
        return None, None

    best_x: int | None = None
    best_ssd = float("inf")

    for xr in range(start_x, end_x + 1):
        right_patch = right_gray[
            y - window_size : y + window_size + 1,
            xr - window_size : xr + window_size + 1,
        ]
        diff = left_patch - right_patch
        ssd = float(np.sum(diff * diff))

        if ssd < best_ssd:
            best_ssd = ssd
            best_x = xr

    if best_x is None:
        return None, None

    return best_x, best_ssd
