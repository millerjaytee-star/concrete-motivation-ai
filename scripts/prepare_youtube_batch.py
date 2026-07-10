#!/usr/bin/env python
"""Prepare the generated YouTube launch videos without publishing publicly."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
MANIFEST_PATH = ROOT / "youtube_launch" / "video_manifest.json"


def load_manifest(path: Path = MANIFEST_PATH) -> list[dict[str, str]]:
    return json.loads(path.read_text(encoding="utf-8"))


def copy_missing_videos(manifest: list[dict[str, str]]) -> list[str]:
    copied: list[str] = []
    for item in manifest:
        destination = ROOT / item["file_path"]
        source = Path(item["source_path"])
        destination.parent.mkdir(parents=True, exist_ok=True)
        if destination.exists():
            continue
        if source.is_file():
            shutil.copy2(source, destination)
            copied.append(str(destination.relative_to(ROOT)))
    return copied


def build_upload_queue(manifest: list[dict[str, str]]) -> list[dict[str, str | bool]]:
    queue: list[dict[str, str | bool]] = []
    for item in manifest:
        if item["visibility"].lower() != "private":
            raise ValueError(f"Refusing non-private YouTube visibility for {item['title']}.")
        video_path = ROOT / item["file_path"]
        queue.append(
            {
                "title": item["title"],
                "file_path": item["file_path"],
                "description": item["description"],
                "visibility": "private",
                "ready": video_path.is_file(),
                "shorts_caption": item["shorts_caption"],
            }
        )
    return queue


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--copy-missing", action="store_true", help="Copy generated videos from the configured source folder.")
    args = parser.parse_args()

    manifest = load_manifest()
    copied = copy_missing_videos(manifest) if args.copy_missing else []
    queue = build_upload_queue(manifest)
    print(json.dumps({"copied": copied, "upload_queue": queue, "safety": "Private upload metadata only. No public publishing performed."}, indent=2))
    return 0 if all(item["ready"] for item in queue) else 1


if __name__ == "__main__":
    raise SystemExit(main())
