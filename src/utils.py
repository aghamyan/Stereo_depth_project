"""Utility helpers for image loading, annotations, and mouse callbacks."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import cv2


def load_image(path: Path) -> Any:
    """Load an image from disk and raise a helpful error when it is missing."""
    image = cv2.imread(str(path))
    if image is None:
        raise FileNotFoundError(f"Could not load image: {path}")
    return image


def create_click_store() -> dict[str, Any]:
    """Create the mutable state shared by OpenCV callbacks."""
    return {
        "left": None,
        "right": None,
        "distance_text": None,
    }


def make_mouse_callback(side: str, store: dict[str, Any]) -> Callable[..., None]:
    """Create a mouse callback that stores the last clicked point for a side."""

    def callback(event: int, x: int, y: int, flags: int, param: Any) -> None:
        del flags, param
        if event == cv2.EVENT_LBUTTONDOWN:
            store[side] = (x, y)

    return callback


def annotate_image(
    image: Any,
    point: tuple[int, int] | None,
    label: str | None = None,
    distance_text: str | None = None,
) -> Any:
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
