#!/usr/bin/env python3
"""Create the Concrete Motivation social sales campaign."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.social_sales_campaign import build_social_sales_campaign, save_social_sales_campaign


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Concrete Motivation social sales campaign.")
    parser.add_argument("--offer", default="Concrete Builders Membership", help="Offer name")
    parser.add_argument("--days", type=int, default=14, help="Campaign length")
    parser.add_argument("--audience", default="Concrete Motivation supporters", help="Audience")
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "outputs" / "social_sales"),
        help="Folder for generated social sales files",
    )
    args = parser.parse_args()

    campaign = build_social_sales_campaign(args.offer, days=args.days, audience=args.audience)
    result = save_social_sales_campaign(campaign, output_dir=Path(args.output_dir))
    print(result.as_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

