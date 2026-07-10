#!/usr/bin/env python3
"""Create a speaker booking revenue package."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.speaker_booking_engine import build_speaker_booking_package, save_speaker_booking_package


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Concrete Motivation speaker booking package.")
    parser.add_argument("--segment", default="schools", help="Booking segment")
    parser.add_argument("--theme", default="Pressure Has a Purpose", help="Speaking theme")
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "outputs" / "speaker_booking"),
        help="Folder for generated speaker booking files",
    )
    args = parser.parse_args()

    package = build_speaker_booking_package(segment=args.segment, theme=args.theme)
    result = save_speaker_booking_package(package, output_dir=Path(args.output_dir))
    print(result.as_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

