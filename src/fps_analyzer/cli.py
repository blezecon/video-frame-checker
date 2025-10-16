import os
import sys
import argparse

# Avoid writing .pyc bytecode files for this process (best-effort).
# For full suppression, run with: python -B ... or set PYTHONDONTWRITEBYTECODE=1
os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
sys.dont_write_bytecode = True

from .ffprobe_stream import has_ffprobe, stream_frame_timestamps
from .analyzer import compute_counts_and_avg
from . import output as out

def main(argv=None) -> int:
    parser = argparse.ArgumentParser(
        description="Count frames per second and average FPS using ffprobe (streams timestamps; low memory)."
    )
    parser.add_argument("input", help="Path to input video file")
    parser.add_argument("--ffprobe", default="ffprobe", help="ffprobe executable (default: ffprobe in PATH)")
    parser.add_argument("--absolute", action="store_true", help="Use absolute seconds (do not normalize start to 0)")
    parser.add_argument(
        "--format",
        choices=["text", "csv", "json"],
        default="text",
        help="Output format (default: text)",
    )
    parser.add_argument(
        "--json-indent",
        type=int,
        default=2,
        help="JSON indent (default: 2)",
    )
    args = parser.parse_args(argv)

    # Check ffprobe first
    if not has_ffprobe(args.ffprobe):
        sys.stderr.write("Error: ffprobe not found. Install FFmpeg and ensure 'ffprobe' is on your PATH.\n")
        return 1

    input_path = args.input
    if not os.path.exists(input_path):
        sys.stderr.write(f"Error: input file not found: {input_path}\n")
        return 1

    try:
        ts_iter = stream_frame_timestamps(input_path, ffprobe_cmd=args.ffprobe)
        stats = compute_counts_and_avg(ts_iter, normalize=(not args.absolute))
        if args.format == "text":
            out.print_text(stats)
        elif args.format == "csv":
            out.print_csv(stats)
        else:
            out.print_json(stats, indent=args.json_indent)
        return 0
    except KeyboardInterrupt:
        sys.stderr.write("\nInterrupted by user.\n")
        return 130
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        return 2

if __name__ == "__main__":
    raise SystemExit(main())