# Stereo Vision Distance Estimation Tool

A simple Python project that estimates distance from a stereo image pair using manually selected corresponding points. The application opens `left.png` and `right.png` from the `data/` directory, lets you click the same feature in both images, then computes disparity and distance with OpenCV and NumPy.

## Project Structure

```text
stereo_depth_project/
│
├── data/
│   ├── left.png
│   └── right.png
│
├── src/
│   ├── main.py
│   ├── stereo.py
│   ├── utils.py
│   └── config.py
│
├── requirements.txt
└── README.md
```

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd src
python main.py
```

## How It Works

1. The program loads `data/left.png` and `data/right.png`.
2. It shows each image in its own OpenCV window.
3. Add your stereo pair as `data/left.png` and `data/right.png`.
4. Click the same point in both images.
5. The program calculates disparity using:

   ```text
   d = |x_left - x_right|
   ```

6. It estimates distance using the stereo vision depth formula:

   ```text
   Z = (f * B) / d
   ```

   Where:
   - `Z` is the distance in meters
   - `f` is focal length in pixels (`800` by default)
   - `B` is the stereo camera baseline in meters (`0.05` by default)
   - `d` is disparity in pixels

7. The console prints:
   - left and right click coordinates
   - disparity
   - computed distance

8. If disparity is zero, the tool returns infinity.

## Usage Notes

- Place your stereo images at `data/left.png` and `data/right.png` before launching the app.
- Click the same point in both images.
- A red marker is drawn at each clicked point.
- The latest computed distance is overlaid on the images briefly before the selection resets.
- Press `q` or `Esc` to quit.

## Data Directory

The repository keeps an empty `data/` directory in version control. Add your own stereo pair as `data/left.png` and `data/right.png` before running the tool.
