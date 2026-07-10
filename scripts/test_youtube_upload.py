#!/usr/bin/env python3
"""Upload one generated video to YouTube privately as a verification test."""

from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.youtube_upload_verification import (
    CONNECT_COMMAND,
    DEFAULT_TEST_DESCRIPTION,
    DEFAULT_TEST_TITLE,
    DEFAULT_TEST_VIDEO,
    DEFAULT_TEST_VISIBILITY,
    VerificationResult,
    build_channel_lookup_command,
    build_upload_command,
    build_verification_package,
    build_upload_result,
    ensure_project_initialized,
    run_command,
)


def print_block(title: str, body: str) -> None:
    print(f"\n{title}\n{'=' * len(title)}")
    print(body)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Concrete Motivation YouTube upload verification.")
    parser.add_argument(
        "--video-path",
        default=str(DEFAULT_TEST_VIDEO),
        help="Single generated video to upload",
    )
    args = parser.parse_args()

    if shutil.which("composio") is None:
        print("Composio CLI was not found on PATH.")
        print(f"Install or activate Composio, then run: {CONNECT_COMMAND}")
        return 127

    project_file = ensure_project_initialized(ROOT)
    if project_file is None:
        print("Composio has not been initialized for this repo.")
        print("Run: composio dev init")
        return 2

    video_path = Path(args.video_path)
    if not video_path.is_file():
        print(f"Video file not found: {video_path}")
        return 2

    package = build_verification_package(video_path)
    print(package.as_markdown())

    connection_check = run_command(["composio", "connections", "list", "--toolkit", "youtube"])
    print_block("Composio Connection Check", connection_check.stdout or connection_check.stderr or "(no output)")
    if connection_check.returncode != 0:
        print(f"YouTube OAuth connection was not confirmed. Exact connect command: {CONNECT_COMMAND}")
        return connection_check.returncode

    upload_command = build_upload_command(package)
    print("Executing upload command:")
    print(" ".join(upload_command))
    upload_result = run_command(upload_command)
    print_block("Upload Output", upload_result.stdout or "(no stdout)")
    if upload_result.stderr.strip():
        print_block("Upload Errors", upload_result.stderr)

    channel_result = run_command(build_channel_lookup_command())
    print_block("Channel Lookup", channel_result.stdout or channel_result.stderr or "(no output)")

    verification = build_upload_result(upload_result.stdout + "\n" + upload_result.stderr, channel_result.stdout + "\n" + channel_result.stderr)
    print(verification.as_markdown())

    if upload_result.returncode != 0:
        print(f"Upload failed. If the account is not connected, run: {CONNECT_COMMAND}")
        return upload_result.returncode

    if not verification.video_id:
        print("Upload completed but a video ID could not be parsed from the Composio response.")
        return 3

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
