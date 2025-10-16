# fps-analyzer (minimal)

Lightweight CLI to count how many video frames occur in each second and compute average FPS.
- Low memory: streams timestamps from `ffprobe` (FFmpeg).
- Works with CFR and VFR.
- Cross-platform: Windows/macOS/Linux.
- No temp files.

## Requirements
- Python 3.8+
- FFmpeg installed (for `ffprobe`)

## Install (editable)
```bash
pip install -e .
```

## Usage
```bash
fps-analyzer input.mp4
# or
python -m fps_analyzer input.mp4
```

### Options
```bash
fps-analyzer INPUT [--ffprobe FFPROBE] [--absolute] [--format {text,csv,json}] [--json-indent 2]
```