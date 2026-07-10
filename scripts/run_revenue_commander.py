#!/usr/bin/env python3
"""Run the Concrete Motivation Revenue Commander."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.revenue_commander import RevenueCommander


def main() -> int:
    parser = argparse.ArgumentParser(description="Run the Concrete Motivation Revenue Commander.")
    parser.add_argument("--theme", default="Concrete Builders Membership", help="Revenue theme")
    parser.add_argument("--monthly-price", type=int, default=40, help="Monthly membership price")
    parser.add_argument("--annual-price", type=int, default=400, help="Annual launch price")
    parser.add_argument("--premium-annual-price", type=int, default=444, help="Premium annual price")
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "outputs" / "revenue_commander"),
        help="Folder for generated revenue commander files",
    )
    args = parser.parse_args()

    result = RevenueCommander(root=Path(args.output_dir)).run(
        args.theme,
        monthly_price=args.monthly_price,
        annual_price=args.annual_price,
        premium_annual_price=args.premium_annual_price,
    )
    print(result.as_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

