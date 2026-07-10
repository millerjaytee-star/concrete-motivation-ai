#!/usr/bin/env python3
"""Create a safe YouTube upload package for Concrete Motivation."""

from __future__ import annotations

import argparse
from concrete_motivation.youtube_publish_package import build_package, save_package


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Concrete Motivation YouTube publishing package.")
    parser.add_argument("topic", help="Video topic or message theme")
    parser.add_argument("--video-path", default="", help="Local video file path to include in package metadata")
    parser.add_argument("--visibility", default="private", choices=["private", "unlisted", "public"], help="YouTube visibility")
    args = parser.parse_args()

    package = build_package(args.topic, video_path=args.video_path, visibility=args.visibility)
    saved = save_package(package)
    print(package.as_markdown())
    print(f"Saved package: {saved}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
