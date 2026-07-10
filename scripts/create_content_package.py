#!/usr/bin/env python3
"""Create one Concrete Motivation content package."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.content_reels_factory import create_content_package


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Concrete Motivation content package.")
    parser.add_argument("topic", help="The message theme or content idea")
    parser.add_argument("--audience", default="", help="Target audience for the package")
    parser.add_argument(
        "--platform",
        default="YouTube, Shorts, Instagram, Facebook, LinkedIn, Podcast",
        help="Primary platform context",
    )
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "outputs" / "content_packages"),
        help="Directory for saved content packages",
    )
    args = parser.parse_args()

    package, export = create_content_package(
        args.topic,
        audience=args.audience,
        platform=args.platform,
        output_dir=Path(args.output_dir),
    )
    print(package.as_markdown())
    print(f"Saved markdown: {export.markdown_path}")
    print(f"Saved json: {export.json_path}")
    print(f"Saved csv: {export.csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

