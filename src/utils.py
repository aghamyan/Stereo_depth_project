"""Utility helpers for image loading, annotations, and mouse callbacks."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

import cv2

MATCH_LINE_COLOR = (0, 255, 255)
LEFT_POINT_COLOR = (0, 0, 255)
RIGHT_POINT_COLOR = (0, 255, 0)

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
        "status_text": "Click a point in the left image to auto-match.",
        "ssd_text": None,
    }

def make_left_mouse_callback(store: dict[str, Any]) -> Callable[..., None]:
    """Create a mouse callback that stores only left-image clicks."""

    def callback(event: int, x: int, y: int, flags: int, param: Any) -> None:
        del flags, param
        if event == cv2.EVENT_LBUTTONDOWN:
            store["left"] = (x, y)

    return callback

def annotate_image(
    image: Any,
    point: tuple[int, int] | None,
    label: str | None = None,
    distance_text: str | None = None,
    status_text: str | None = None,
    epipolar_y: int | None = None,
    match_point: tuple[int, int] | None = None,
    ssd_text: str | None = None,
) -> Any:
    """Return a copy of the image annotated with points, labels, and guide lines."""
    annotated = image.copy()

    if epipolar_y is not None:
        cv2.line(
            annotated,
            (0, epipolar_y),
            (annotated.shape[1] - 1, epipolar_y),
            MATCH_LINE_COLOR,
            1,
            cv2.LINE_AA,
        )

    if point is not None:
        cv2.circle(annotated, point, 6, LEFT_POINT_COLOR, -1)
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

    if match_point is not None:
        cv2.circle(annotated, match_point, 6, RIGHT_POINT_COLOR, -1)
        cv2.circle(annotated, match_point, 14, (255, 255, 255), 2)
        cv2.putText(
            annotated,
            label or f"({match_point[0]}, {match_point[1]})",
            (match_point[0] + 10, match_point[1] - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (20, 20, 20),
            2,
            cv2.LINE_AA,
        )

    overlay_lines = [line for line in (distance_text, ssd_text, status_text) if line]
    for index, text in enumerate(overlay_lines):
        y = 35 + (index * 28)
        cv2.putText(
            annotated,
            text,
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (0, 0, 0),
            3,
            cv2.LINE_AA,
        )
        cv2.putText(
            annotated,
            text,
            (20, y),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.75,
            (255, 255, 255),
            1,
            cv2.LINE_AA,
        )

    return annotated
