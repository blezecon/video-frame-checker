import json
from .analyzer import FrameStats

def print_text(stats: FrameStats) -> None:
    header = (
        "Per-second frame counts (seconds start at 0)"
        if stats.normalized_start
        else "Per-second frame counts (absolute seconds)"
    )
    print(header)
    for sec in sorted(stats.per_second_counts):
        print(f"second {sec}: {stats.per_second_counts[sec]} frames")

    print("\nSummary")
    print(f"- Total frames: {stats.total_frames}")
    print(f"- Duration (from timestamps): {stats.duration_s:.6f} s")
    print(f"- Average FPS (from timestamps): {stats.average_fps:.6f}")

def print_csv(stats: FrameStats) -> None:
    print("second,frames")
    for sec in sorted(stats.per_second_counts):
        print(f"{sec},{stats.per_second_counts[sec]}")
    print(f"# total_frames,{stats.total_frames}")
    print(f"# duration_seconds_from_timestamps,{stats.duration_s:.6f}")
    print(f"# average_fps_from_timestamps,{stats.average_fps:.6f}")

def print_json(stats: FrameStats, indent: int = 2) -> None:
    data = {
        "normalize_start": stats.normalized_start,
        "summary": {
            "total_frames": stats.total_frames,
            "duration_seconds_from_timestamps": stats.duration_s,
            "average_fps_from_timestamps": stats.average_fps,
            "first_timestamp": stats.first_timestamp,
            "last_timestamp": stats.last_timestamp,
        },
        "per_second": [
            {"second": sec, "frames": stats.per_second_counts[sec]}
            for sec in sorted(stats.per_second_counts)
        ],
    }
    print(json.dumps(data, indent=indent))