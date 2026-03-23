"""Interactive stereo vision distance estimation entry point."""

from __future__ import annotations

try:
    import cv2
except ModuleNotFoundError:
    print("OpenCV (cv2) is not installed. Install with: pip install opencv-python")
    raise SystemExit(1)

from src.config import (
    BASELINE,
    FOCAL_LENGTH,
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

    cv2.namedWindow(WINDOW_LEFT)
    cv2.namedWindow(WINDOW_RIGHT)
    cv2.setMouseCallback(WINDOW_LEFT, make_mouse_callback("left", click_store))
    cv2.setMouseCallback(WINDOW_RIGHT, make_mouse_callback("right", click_store))

    print("Stereo vision distance estimation tool")
    print("Run with your virtual environment active: python -m src.main")
    print("Click the same point in both images. Press 'q' or ESC to quit.")

    while True:
        left_view = annotate_image(
            left_image,
            click_store["left"],
            label="Left point",
            distance_text=click_store["distance_text"],
        )
        right_view = annotate_image(
            right_image,
            click_store["right"],
            label="Right point",
            distance_text=click_store["distance_text"],
        )

        cv2.imshow(WINDOW_LEFT, left_view)
        cv2.imshow(WINDOW_RIGHT, right_view)

        if click_store["left"] is not None and click_store["right"] is not None:
            x_left, y_left = click_store["left"]
            x_right, y_right = click_store["right"]
            disparity = compute_disparity(x_left, x_right)
            distance = compute_distance(disparity, FOCAL_LENGTH, BASELINE)
            click_store["distance_text"] = format_distance(distance)

            print(f"Left click:  ({x_left}, {y_left})")
            print(f"Right click: ({x_right}, {y_right})")
            print(f"Disparity:   {disparity} pixels")
            if distance == float("inf"):
                print("Distance:    infinity (zero disparity)")
            else:
                print(f"Distance:    {distance:.3f} meters")
            print("-" * 40)

            cv2.imshow(
                WINDOW_LEFT,
                annotate_image(left_image, click_store["left"], "Left point", click_store["distance_text"]),
            )
            cv2.imshow(
                WINDOW_RIGHT,
                annotate_image(right_image, click_store["right"], "Right point", click_store["distance_text"]),
            )
            cv2.waitKey(500)

            click_store["left"] = None
            click_store["right"] = None

        key = cv2.waitKey(20) & 0xFF
        if key in QUIT_KEYS:
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
