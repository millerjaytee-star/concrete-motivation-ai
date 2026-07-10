#!/usr/bin/env python3
"""Create a Concrete Motivation podcast guest campaign."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.podcast_guest_bot import PodcastGuestBot


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Concrete Motivation podcast guest campaign.")
    parser.add_argument("--theme", default="pressure to purpose", help="Guest outreach theme")
    parser.add_argument("--audience", default="leaders and creators", help="Target audience")
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "outputs" / "podcast_production" / "guest_outreach"),
        help="Folder for generated campaign files",
    )
    args = parser.parse_args()

    result = PodcastGuestBot(root=Path(args.output_dir)).run(args.theme, args.audience)
    print(result.as_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

