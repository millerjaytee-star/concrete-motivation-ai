#!/usr/bin/env python3
"""Execute a confirmed Composio YouTube upload after explicit typed approval."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.youtube_publish_package import build_execute_command, build_package, save_package

CONFIRMATION_TEXT = "UPLOAD TO YOUTUBE"
CONNECT_COMMAND = "composio link youtube"


def run_command(command: list[str]) -> int:
    try:
        completed = subprocess.run(command, check=False, capture_output=True, text=True)
    except FileNotFoundError:
        print("Composio CLI was not found on PATH.")
        print("Install or activate Composio, then rerun this script.")
        return 127

    if completed.stdout.strip():
        print(completed.stdout.strip())
    if completed.stderr.strip():
        print(completed.stderr.strip())
    return completed.returncode


def main() -> int:
    parser = argparse.ArgumentParser(description="Upload a Concrete Motivation video to YouTube via Composio.")
    parser.add_argument("topic", help="Video topic or message theme")
    parser.add_argument("--video-path", required=True, help="Local video file path to upload")
    parser.add_argument("--visibility", default="private", choices=["private", "unlisted", "public"], help="YouTube visibility")
    args = parser.parse_args()

    confirmation = input(f'Type "{CONFIRMATION_TEXT}" to continue: ').strip()
    if confirmation != CONFIRMATION_TEXT:
        print("Upload cancelled.")
        return 1

    video_path = Path(args.video_path)
    package = build_package(args.topic, video_path=str(video_path), visibility=args.visibility)
    saved = save_package(package)
    command = build_execute_command(package)

    print(package.as_markdown())
    print(f"Saved package: {saved}")
    print("Executing:")
    print(" ".join(command))

    exit_code = run_command(command)
    if exit_code != 0:
        print(f"YouTube upload did not complete successfully. If the account is not connected, run: {CONNECT_COMMAND}")
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
