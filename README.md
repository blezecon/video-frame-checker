# video-frame-checker (fps-analyzer)

Lightweight CLI to count how many video frames occur in each second and compute average FPS using ffprobe (FFmpeg).
- Low memory: streams timestamps; works on CFR and VFR.
- Cross‑platform: Linux/macOS/Windows.
- No temp/cache files.

## Requirements

- Python 3.8+ (works with 3.13 as well)
- FFmpeg installed (for `ffprobe`)
  - Ubuntu/Debian: `sudo apt-get update && sudo apt-get install -y ffmpeg`
  - Fedora: `sudo dnf install ffmpeg`
  - Arch: `sudo pacman -S ffmpeg`
  - macOS (Homebrew): `brew install ffmpeg`
  - Verify: `ffprobe -version`

## Project layout

```text
project-root/
├── pyproject.toml
├── README.md
└── src/
    └── fps_analyzer/
        ├── __init__.py
        ├── __main__.py
        ├── cli.py
        ├── ffprobe_stream.py
        ├── analyzer.py
        └── output.py
```

## Setup a virtual environment (venv) and install

Do these from your project root (where `pyproject.toml` is).

### Linux/macOS (bash/zsh)

```bash
# 1) Create venv
python3 -m venv .venv

# 2) Activate venv
source .venv/bin/activate

# 3) Upgrade pip (optional but recommended)
python -m pip install -U pip

# 4) Install this project in editable mode (so changes in src/ take effect immediately)
pip install -e .
```

Fish shell:

```fish
python3 -m venv .venv
source .venv/bin/activate.fish
python -m pip install -U pip
pip install -e .
```

### Windows (PowerShell)

```powershell
# 1) Create venv
py -m venv .venv

# 2) Activate venv
.\.venv\Scripts\Activate.ps1

# 3) Upgrade pip (optional)
python -m pip install -U pip

# 4) Install this project (editable)
pip install -e .
```

### Verify you’re using the venv

```bash
which python
which pip
python --version
pip --version
```

On Windows PowerShell:

```powershell
Get-Command python
Get-Command pip
python --version
pip --version
```

You should see paths inside `.venv`.

## Run the tool

- Using the console script (preferred):

```bash
fps-analyzer "/run/media/blezecon/hdd/Obs/test1.mp4"
```

- Or run as a Python module:

```bash
python -m fps_analyzer "/run/media/blezecon/hdd/Obs/test1.mp4"
```

### Output formats and options

```bash
# JSON output
fps-analyzer "/run/media/blezecon/hdd/Obs/test1.mp4" --format json

# CSV output
fps-analyzer "/run/media/blezecon/hdd/Obs/test1.mp4" --format csv

# Use absolute seconds instead of starting at 0
fps-analyzer "/run/media/blezecon/hdd/Obs/test1.mp4" --absolute
```

## Troubleshooting

- ffprobe not found
  - Install FFmpeg and ensure `ffprobe` is on your PATH.
  - Check with: `ffprobe -version`

- Command not found: fps-analyzer
  - Ensure your venv is activated and you ran `pip install -e .`
  - Alternatively run: `python -m fps_analyzer "path/to/file"`

- No module named python
  - You probably ran `-m python -m pip ...`. Use: `python -m pip ...` (single `-m`).

- Input file not found
  - Double-check the exact filename and keep the path in quotes.

## Deactivate the venv

```bash
deactivate
```

## Notes

- The tool does a single streaming pass over the video; memory use is low and it works on low‑end CPUs.
- To completely avoid `.pyc` files, you can run with `python -B -m fps_analyzer "<file>"`.