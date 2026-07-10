#!/usr/bin/env python
"""Private-only YouTube upload verification harness.

By default this performs a dry run. It will not upload unless --execute is used
and CONCRETE_ALLOW_YOUTUBE_UPLOAD_PRIVATE=yes is set.
"""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

VIDEO_PATH = Path("generated_videos/01_built_under_pressure.mp4")
TITLE = "Built Under Pressure"
DESCRIPTION = "Test upload from Concrete Motivation AI Operating System."
VISIBILITY = "private"


def build_payload(video_path: Path) -> dict[str, object]:
    return {
        "file_path": str(video_path),
        "title": TITLE,
        "description": DESCRIPTION,
        "privacy_status": VISIBILITY,
        "visibility": VISIBILITY,
    }


def validate_single_private_upload(video_path: Path, visibility: str) -> None:
    if visibility.lower() != VISIBILITY:
        raise ValueError("YouTube verification uploads must stay PRIVATE.")
    if video_path != VIDEO_PATH:
        raise ValueError(f"Refusing to upload anything except {VIDEO_PATH}.")
    if not video_path.is_file():
        raise FileNotFoundError(f"Expected video not found: {video_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true", help="Perform the one private upload through Composio.")
    parser.add_argument("--tool-slug", default="YOUTUBE_UPLOAD_VIDEO", help="Composio YouTube upload tool slug.")
    args = parser.parse_args()

    payload = build_payload(VIDEO_PATH)

    if not args.execute:
        upload_status = "dry_run_ready" if VIDEO_PATH.is_file() else "dry_run_missing_video"
        print(
            json.dumps(
                {
                    "upload_status": upload_status,
                    "video_id": None,
                    "video_url": None,
                    "channel_name": None,
                    "metadata": payload,
                    "safety": "No upload performed. Visibility locked to PRIVATE.",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    validate_single_private_upload(VIDEO_PATH, VISIBILITY)

    if os.environ.get("CONCRETE_ALLOW_YOUTUBE_UPLOAD_PRIVATE") != "yes":
        raise PermissionError("Set CONCRETE_ALLOW_YOUTUBE_UPLOAD_PRIVATE=yes to allow the single private upload.")

    command = ["composio", "execute", args.tool_slug, "-d", json.dumps(payload)]
    result = subprocess.run(command, check=False, capture_output=True, text=True)
    print(result.stdout.strip() or result.stderr.strip())
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
