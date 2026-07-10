#!/usr/bin/env python3
"""Preview the exact Composio YouTube upload command without uploading."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.youtube_publish_package import build_execute_command, build_package, save_package


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview a Concrete Motivation YouTube upload.")
    parser.add_argument("topic", help="Video topic or message theme")
    parser.add_argument("--video-path", required=True, help="Local video file path to preview")
    parser.add_argument("--visibility", default="private", choices=["private", "unlisted", "public"], help="YouTube visibility")
    args = parser.parse_args()

    video_path = Path(args.video_path)
    package = build_package(args.topic, video_path=str(video_path), visibility=args.visibility)
    saved = save_package(package)
    command = build_execute_command(package)

    print(package.as_markdown())
    print("Dry run command:")
    print(" ".join(command))
    print(f"Saved package: {saved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
