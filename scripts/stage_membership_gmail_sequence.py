#!/usr/bin/env python3
"""Stage membership Gmail drafts without sending them."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.gmail_sales_stager import build_gmail_sales_sequence, save_gmail_sales_sequence


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage the Concrete Builders Membership Gmail sequence.")
    parser.add_argument("--offer", default="Concrete Builders Membership", help="Membership offer")
    parser.add_argument("--audience", default="Concrete Motivation supporters", help="Audience")
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "outputs" / "gmail_staging" / "membership"),
        help="Folder for staged Gmail drafts",
    )
    args = parser.parse_args()

    sequence = build_gmail_sales_sequence(args.offer, audience=args.audience)
    result = save_gmail_sales_sequence(sequence, output_dir=Path(args.output_dir))
    print(result.as_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

