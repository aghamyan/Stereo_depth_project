"""Utility helpers for image loading, annotations, and mouse callbacks."""

from __future__ import annotations

from typing import Callable

import cv2
import numpy as np


def load_image(path):
    """Load an image from disk and raise a helpful error when it is missing."""
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Could not load image: {path}")
    return image



def create_click_store() -> dict:
    """Create the mutable state shared by OpenCV callbacks."""
    return {
        "left": None,
        "right": None,
        "distance_text": None,
    }



def make_mouse_callback(side: str, store: dict) -> Callable:
    """Create a mouse callback that stores the last clicked point for a side."""

    def callback(event, x, y, flags, param):
        del flags, param
        if event == cv2.EVENT_LBUTTONDOWN:
            store[side] = (x, y)

    return callback



def annotate_image(image: np.ndarray, point, label: str | None = None, distance_text: str | None = None) -> np.ndarray:
    """Return a copy of the image annotated with the clicked point and labels."""
    annotated = image.copy()

    if point is not None:
        cv2.circle(annotated, point, 6, (0, 0, 255), -1)
        cv2.circle(annotated, point, 14, (255, 255, 255), 2)
        point_label = label or f"({point[0]}, {point[1]})"
        cv2.putText(
            annotated,
            point_label,
            (point[0] + 10, point[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (20, 20, 20),
            2,
            cv2.LINE_AA,
        )

    if distance_text:
        cv2.putText(
            annotated,
            distance_text,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.85,
            (0, 0, 0),
            3,
            cv2.LINE_AA,
        )
        cv2.putText(
            annotated,
            distance_text,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.85,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

    return annotated
