#!/usr/bin/env python3
"""Report the ffmpeg binary that Concrete Motivation will use locally."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.ffmpeg_tools import configure_imageio_ffmpeg, ffmpeg_status


def main() -> int:
    parser = argparse.ArgumentParser(description="Check local ffmpeg availability.")
    parser.add_argument(
        "--ffmpeg-bin",
        default=os.getenv("CONCRETE_MOTIVATION_FFMPEG_BIN", ""),
        help="Preferred ffmpeg binary path or directory",
    )
    args = parser.parse_args()

    resolved = configure_imageio_ffmpeg(args.ffmpeg_bin or None)
    status = ffmpeg_status(args.ffmpeg_bin or None)
    print(status.as_markdown())

    if resolved.is_file():
        try:
            completed = subprocess.run(
                [str(resolved), "-version"],
                check=False,
                capture_output=True,
                text=True,
            )
            version_line = completed.stdout.splitlines()[0] if completed.stdout else ""
            if version_line:
                print(f"\nVersion: {version_line}")
        except OSError as exc:
            print(f"\nVersion check failed: {exc}")

    return 0 if status.available else 1


if __name__ == "__main__":
    raise SystemExit(main())
