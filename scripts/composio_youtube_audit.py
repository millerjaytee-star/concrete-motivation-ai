"""Audit the connected Composio YouTube account.

Run from the project root:
    python3 scripts/composio_youtube_audit.py

This script calls the local Composio CLI that is already logged in on your Mac.
It checks the active connections and tries the YouTube channel queries with the
parameters your CLI accepted during setup.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path
from typing import Any

OUT_DIR = Path("reports/composio")


def run_command(command: list[str]) -> dict[str, Any]:
    print("\n$ " + " ".join(command))
    completed = subprocess.run(command, capture_output=True, text=True, check=False, timeout=60)
    print(completed.stdout)
    if completed.stderr:
        print(completed.stderr)
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def save(name: str, payload: dict[str, Any]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / name
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    print(f"Saved {path}")


def main() -> None:
    if shutil.which("composio") is None:
        raise SystemExit("Composio CLI was not found. Install it and log in before running this audit.")

    checks = {
        "01_whoami.json": ["composio", "whoami"],
        "02_connections.json": ["composio", "connections", "list"],
        "03_youtube_channels_snippet.json": [
            "composio",
            "execute",
            "YOUTUBE_LIST_CHANNELS",
            "-d",
            '{"mine": true, "part": "snippet"}',
        ],
        "04_youtube_channels_statistics.json": [
            "composio",
            "execute",
            "YOUTUBE_LIST_CHANNELS",
            "-d",
            '{"mine": true, "part": "statistics"}',
        ],
        "05_youtube_channel_videos.json": [
            "composio",
            "execute",
            "YOUTUBE_LIST_CHANNEL_VIDEOS",
            "-d",
            '{"mine": true}',
        ],
    }
    results: dict[str, Any] = {}
    for filename, command in checks.items():
        result = run_command(command)
        save(filename, result)
        results[filename] = result

    summary = OUT_DIR / "README.md"
    summary.write_text(
        "# Composio YouTube Audit\n\n"
        "Review the JSON files in this folder. If YouTube returns totalResults: 0, "
        "the connected Google account may not expose a YouTube channel through this endpoint, "
        "or the current Composio YouTube toolkit may only have read/list permissions.\n",
        encoding="utf-8",
    )
    print(f"Saved {summary}")


if __name__ == "__main__":
    main()
