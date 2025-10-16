# fps-analyzer

Lightweight CLI to count how many video frames occur in each second and compute average FPS.
- Low memory: streams timestamps from `ffprobe` (FFmpeg).
- Works with CFR and VFR.
- Cross-platform: Windows/macOS/Linux.
- No temp files. You can also run with `-B` (or set `PYTHONDONTWRITEBYTECODE=1`) to avoid `.pyc` caches.

## Requirements
- FFmpeg installed (for `ffprobe`).
  - Windows: install a static build and add `bin` to PATH (e.g., Gyan.dev or BtbN), or `winget install Gyan.FFmpeg`
  - macOS: `brew install ffmpeg`
  - Ubuntu/Debian: `sudo apt-get update && sudo apt-get install -y ffmpeg`
  - Fedora: `sudo dnf install ffmpeg`
- Python 3.8+

## Install (editable local)
```bash
pip install -e .
```

## Usage
- CLI (installed via entry point):
  ```bash
  fps-analyzer input.mp4
  ```
- Module:
  ```bash
  python -m fps_analyzer input.mp4
  ```
- Disable `.pyc` bytecode:
  ```bash
  PYTHONDONTWRITEBYTECODE=1 fps-analyzer input.mp4
  # or
  python -B -m fps_analyzer input.mp4
  ```

### Options
```bash
fps-analyzer INPUT [--ffprobe FFPROBE] [--absolute] [--format {text,csv,json}]
```
- `--ffprobe`: path to ffprobe (default: `ffprobe` in PATH)
- `--absolute`: don't normalize timestamps to start at 0
- `--format`: output format (default `text`; also `csv`, `json`)

### Output example (text)
```
Per-second frame counts (seconds start at 0)
second 0: 30 frames
second 1: 30 frames
...

Summary
- Total frames: 900
- Duration (from timestamps): 30.000000 s
- Average FPS (from timestamps): 30.000000
```

## Notes
- Average FPS is computed from timestamps: `total_frames / (last_ts - first_ts)`.
- For short clips where duration collapses to ~0, we fall back to a count-based estimate.
- No temp files are written. To fully avoid `.pyc` caches, use `python -B` or set `PYTHONDONTWRITEBYTECODE=1`.