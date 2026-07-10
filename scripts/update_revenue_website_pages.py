#!/usr/bin/env python3
"""Write the revenue website pages to website_content/."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.revenue_website_pages import save_revenue_website_pages


def main() -> int:
    parser = argparse.ArgumentParser(description="Update the Concrete Motivation revenue website pages.")
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "website_content"),
        help="Folder for generated website content pages",
    )
    parser.add_argument("--offer", default="Concrete Builders Membership", help="Membership offer")
    parser.add_argument("--monthly-price", type=int, default=40, help="Monthly price")
    parser.add_argument("--annual-price", type=int, default=400, help="Annual price")
    parser.add_argument("--premium-annual-price", type=int, default=444, help="Premium annual price")
    args = parser.parse_args()

    result = save_revenue_website_pages(
        output_dir=Path(args.output_dir),
        offer=args.offer,
        monthly_price=args.monthly_price,
        annual_price=args.annual_price,
        premium_annual_price=args.premium_annual_price,
    )
    print(result.as_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

