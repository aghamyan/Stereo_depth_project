"""Configuration values for the stereo depth project."""

from pathlib import Path

BASELINE = 0.04
FIELD_OF_VIEW_DEGREES = 75
IMAGE_WIDTH = 640

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LEFT_IMAGE_PATH = DATA_DIR / "left.png"
RIGHT_IMAGE_PATH = DATA_DIR / "right.png"
WINDOW_LEFT = "Left Image"
WINDOW_RIGHT = "Right Image"
QUIT_KEYS = {27, ord("q")}
