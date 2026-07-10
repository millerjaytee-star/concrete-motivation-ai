#!/usr/bin/env python3
"""Create a 30-day Concrete Motivation content batch."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.content_batch_runner import create_30_day_content_batch


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Concrete Motivation 30-day content batch.")
    parser.add_argument("--theme", required=True, help="Theme for the 30-day batch")
    parser.add_argument("--audience", default="", help="Target audience for the batch")
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "outputs" / "content_packages"),
        help="Directory for saved content packages",
    )
    args = parser.parse_args()

    result = create_30_day_content_batch(args.theme, audience=args.audience, output_dir=Path(args.output_dir))
    print(result.as_markdown())
    for export in result.exports:
        print(f"Saved package: {export.folder}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

