"""Interactive stereo vision distance estimation entry point."""

from __future__ import annotations

import cv2

from src.config import (
    BASELINE,
    FIELD_OF_VIEW_DEGREES,
    IMAGE_WIDTH,
    LEFT_IMAGE_PATH,
    QUIT_KEYS,
    RIGHT_IMAGE_PATH,
    WINDOW_LEFT,
    WINDOW_RIGHT,
)
from src.stereo import compute_disparity, compute_distance
from src.utils import annotate_image, create_click_store, load_image, make_mouse_callback


def format_distance(distance: float) -> str:
    """Format distance text for console and image annotations."""
    if distance == float("inf"):
        return "Distance: infinity (zero disparity)"
    return f"Distance: {distance:.3f} m"


def main() -> None:
    """Run the stereo depth estimation application."""
    try:
        left_image = load_image(LEFT_IMAGE_PATH)
        right_image = load_image(RIGHT_IMAGE_PATH)
    except FileNotFoundError as error:
        print(f"Error: {error}")
        raise SystemExit(1) from error

    click_store = create_click_store()
    last_processed_pair: tuple[tuple[int, int], tuple[int, int]] | None = None

    cv2.namedWindow(WINDOW_LEFT)
    cv2.namedWindow(WINDOW_RIGHT)
    cv2.setMouseCallback(WINDOW_LEFT, make_mouse_callback(click_store, side="left"))
    cv2.setMouseCallback(WINDOW_RIGHT, make_mouse_callback(click_store, side="right"))

    print("Stereo vision distance estimation tool")
    print("Run with your virtual environment active: python main.py")
    print("Click corresponding objects in the LEFT and RIGHT images to measure distance.")
    print("Press 'q' or ESC to quit.")

    while True:
        left_point = click_store["left"]
        right_point = click_store["right"]
        selected_pair = (
            (left_point, right_point)
            if left_point is not None and right_point is not None
            else None
        )

        if selected_pair is not None and selected_pair != last_processed_pair:
            (x_left, y_left), (x_right, y_right) = selected_pair
            last_processed_pair = selected_pair

            disparity = compute_disparity(x_left, x_right)
            distance = compute_distance(
                x_left,
                x_right,
                IMAGE_WIDTH,
                FIELD_OF_VIEW_DEGREES,
                BASELINE,
            )
            click_store["distance_text"] = format_distance(distance)
            click_store["status_text"] = "Measurement updated. Click either image to select a new pair."

            print(f"Left point:  ({x_left}, {y_left})")
            print(f"Right point: ({x_right}, {y_right})")
            print(f"Disparity:   {disparity} pixels")
            if distance == float("inf"):
                print("Distance:    infinity (zero disparity)")
            else:
                print(f"Distance:    {distance:.3f} meters")
            print("-" * 40)

        left_view = annotate_image(
            left_image,
            left_point,
            label="Left point",
            distance_text=click_store["distance_text"],
            status_text=click_store["status_text"],
            epipolar_y=left_point[1] if left_point else None,
        )
        right_view = annotate_image(
            right_image,
            right_point,
            label="Right point",
            distance_text=click_store["distance_text"],
            status_text=click_store["status_text"],
            epipolar_y=right_point[1] if right_point else None,
        )

        cv2.imshow(WINDOW_LEFT, left_view)
        cv2.imshow(WINDOW_RIGHT, right_view)

        key = cv2.waitKey(20) & 0xFF
        if key in QUIT_KEYS:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
