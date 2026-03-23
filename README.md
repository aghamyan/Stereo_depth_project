# Stereo Vision Distance Estimation Tool

A small stereo-vision application that loads a left/right image pair, lets you manually click corresponding points in the left and right images, then computes depth with angle-based triangulation derived from the camera field of view and baseline. The project is structured as a Python package so it is run consistently with `python -m src.main` from an activated virtual environment.

## Final Folder Structure

```text
stereo_depth_project/
├── data/
│   ├── left.png
│   └── right.png
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── stereo.py
│   └── utils.py
├── requirements.txt
└── README.md
```

## Setup and Run

### 1. Create a virtual environment

```bash
python3 -m venv .venv
```

### 2. Activate the virtual environment

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 4. Run the project

```bash
python -m src.main
```

## Notes

- Do not run `python src/main.py`; the supported entry point is `python -m src.main`.
- Keep your virtual environment activated so `python` resolves to the environment interpreter rather than `/usr/bin/python3`.
- If OpenCV is missing, the app exits cleanly and prints: `Install with: pip install opencv-python`.
- Place your stereo images at `data/left.png` and `data/right.png` before starting the app.
- Distance is computed from the manually selected left/right x-coordinates using a 75° horizontal field of view, 640-pixel image width, and 0.04 m camera baseline.
