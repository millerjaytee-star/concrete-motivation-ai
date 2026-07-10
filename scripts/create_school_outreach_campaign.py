#!/usr/bin/env python3
"""Create a Concrete Motivation school outreach campaign."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.school_outreach_bot import SchoolOutreachBot


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Concrete Motivation school outreach campaign.")
    parser.add_argument("--audience", default="high school athletes", help="Target audience")
    parser.add_argument("--region", default="", help="Target region")
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "outputs" / "outreach_messages" / "school_outreach"),
        help="Folder for generated campaign files",
    )
    args = parser.parse_args()

    result = SchoolOutreachBot(root=Path(args.output_dir)).run("Pressure Has a Purpose", args.audience, args.region)
    print(result.as_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

