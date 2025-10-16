import math
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Dict, Iterable, Optional

@dataclass
class FrameStats:
    per_second_counts: Dict[int, int] = field(default_factory=dict)
    total_frames: int = 0
    duration_s: float = 0.0
    average_fps: float = 0.0
    first_timestamp: Optional[float] = None
    last_timestamp: Optional[float] = None
    normalized_start: bool = True

def compute_counts_and_avg(
    timestamps: Iterable[float],
    normalize: bool = True,
    eps: float = 1e-9,
) -> FrameStats:
    counts: Dict[int, int] = defaultdict(int)
    total_frames = 0
    t0: Optional[float] = None
    t_last: Optional[float] = None

    for t in timestamps:
        if t0 is None:
            t0 = t
        t_rel = (t - t0) if normalize else t
        # Fix tiny negatives from floating error
        if -1e-6 < t_rel < 0:
            t_rel = 0.0
        if t_rel < 0:
            # Skip truly negative times
            continue

        sec_bin = int(math.floor(t_rel + eps))  # place into [sec, sec+1)
        counts[sec_bin] += 1
        total_frames += 1
        t_last = t

    duration_s = 0.0
    avg_fps = 0.0
    if t0 is not None and t_last is not None:
        # Duration from timestamps
        duration_s = max(0.0, t_last - t0) if normalize else max(0.0, t_last - (min(counts) if counts else 0))
        if duration_s > 0 and total_frames > 0:
            avg_fps = total_frames / duration_s
        elif total_frames > 0:
            # Fallback: infer duration from bins for extremely short clips
            max_sec = max(counts) if counts else 0
            duration_s = max(1.0, float(max_sec + 1))
            avg_fps = total_frames / duration_s

    return FrameStats(
        per_second_counts=dict(counts),
        total_frames=total_frames,
        duration_s=duration_s,
        average_fps=avg_fps,
        first_timestamp=t0,
        last_timestamp=t_last,
        normalized_start=normalize,
    )