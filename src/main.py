"""Interactive stereo vision distance estimation entry point."""

from __future__ import annotations

try:
    import cv2
except ModuleNotFoundError:
    print("OpenCV (cv2) is not installed. Install with: pip install opencv-python")
    raise SystemExit(1)

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
from src.stereo import compute_disparity, compute_distance, find_match
from src.utils import annotate_image, create_click_store, load_image, make_left_mouse_callback

WINDOW_SIZE = 5
SEARCH_RANGE = 100

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
    last_processed_left = None

    cv2.namedWindow(WINDOW_LEFT)
    cv2.namedWindow(WINDOW_RIGHT)
    cv2.setMouseCallback(WINDOW_LEFT, make_left_mouse_callback(click_store))

    print("Stereo vision distance estimation tool")
    print("Run with your virtual environment active: python main.py")
    print("Click a point in the LEFT image to automatically find its match in the RIGHT image.")
    print("Press 'q' or ESC to quit.")

    while True:
        left_point = click_store["left"]
        right_point = click_store["right"]

        if left_point is not None and left_point != last_processed_left:
            x_left, y_left = left_point
            matched_x, best_ssd = find_match(
                left_image,
                right_image,
                x_left,
                y_left,
                window_size=WINDOW_SIZE,
                search_range=SEARCH_RANGE,
            )
            last_processed_left = left_point

            if matched_x is None:
                click_store["right"] = None
                click_store["distance_text"] = None
                click_store["ssd_text"] = None
                click_store["status_text"] = "Warning: no valid match found for that point."
                print(f"Left point: ({x_left}, {y_left})")
                print("Warning: no valid match found.")
                print("-" * 40)
            else:
                x_right = matched_x
                y_right = y_left
                click_store["right"] = (x_right, y_right)

                disparity = compute_disparity(x_left, x_right)
                distance = compute_distance(
                    x_left,
                    x_right,
                    IMAGE_WIDTH,
                    FIELD_OF_VIEW_DEGREES,
                    BASELINE,
                )
                click_store["distance_text"] = format_distance(distance)
                click_store["ssd_text"] = f"Best SSD: {best_ssd:.2f}"
                click_store["status_text"] = "Auto-match complete. Click another point in the left image."

                print(f"Left point:    ({x_left}, {y_left})")
                print(f"Matched point: ({x_right}, {y_right})")
                print(f"Disparity:     {disparity} pixels")
                print(f"Best SSD:      {best_ssd:.2f}")
                if distance == float("inf"):
                    print("Distance:      infinity (zero disparity)")
                else:
                    print(f"Distance:      {distance:.3f} meters")
                print("-" * 40)

        left_view = annotate_image(
            left_image,
            left_point,
            label="Left point",
            distance_text=click_store["distance_text"],
            status_text=click_store["status_text"],
            epipolar_y=left_point[1] if left_point else None,
            ssd_text=click_store["ssd_text"],
        )
        right_view = annotate_image(
            right_image,
            None,
            label="Matched point",
            distance_text=click_store["distance_text"],
            status_text=click_store["status_text"],
            epipolar_y=right_point[1] if right_point else (left_point[1] if left_point else None),
            match_point=right_point,
            ssd_text=click_store["ssd_text"],
        )

        cv2.imshow(WINDOW_LEFT, left_view)
        cv2.imshow(WINDOW_RIGHT, right_view)

        key = cv2.waitKey(20) & 0xFF
        if key in QUIT_KEYS:
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
