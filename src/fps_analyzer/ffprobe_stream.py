import subprocess
import math
from typing import Iterator, Optional

def has_ffprobe(ffprobe_cmd: str) -> bool:
    try:
        subprocess.run(
            [ffprobe_cmd, "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True,
        )
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        return False

def stream_frame_timestamps(input_path: str, ffprobe_cmd: str = "ffprobe") -> Iterator[float]:
    """
    Yields frame timestamps (float seconds) from ffprobe.
    Tries best_effort_timestamp_time, then pkt_pts_time; both may be "N/A".
    """
    cmd = [
        ffprobe_cmd,
        "-v", "error",
        "-select_streams", "v:0",
        "-show_frames",
        "-show_entries", "frame=best_effort_timestamp_time,pkt_pts_time",
        "-of", "csv=p=0",
        input_path,
    ]

    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,  # line-buffered
    )

    try:
        assert proc.stdout is not None
        for line in proc.stdout:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            ts: Optional[float] = None
            for val in parts:
                if val and val != "N/A":
                    try:
                        ts = float(val)
                        break
                    except ValueError:
                        continue
            if ts is not None and math.isfinite(ts):
                yield ts

        # Drain stderr and check return code to surface errors
        err = proc.stderr.read() if proc.stderr else ""
        ret = proc.wait()
        if ret != 0:
            raise RuntimeError(f"ffprobe exited with status {ret}. stderr:\n{err}")
    finally:
        try:
            proc.kill()
        except Exception:
            pass
        try:
            proc.stdout and proc.stdout.close()
        except Exception:
            pass
        try:
            proc.stderr and proc.stderr.close()
        except Exception:
            pass