#!/usr/bin/env python3
"""Create the Concrete Builders Membership program package."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.membership_program import build_membership_program, save_membership_program


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the Concrete Builders Membership program.")
    parser.add_argument("--offer", default="Concrete Builders Membership", help="Membership offer name")
    parser.add_argument("--monthly-price", type=int, default=40, help="Monthly price")
    parser.add_argument("--annual-price", type=int, default=400, help="Launch annual price")
    parser.add_argument("--premium-annual-price", type=int, default=444, help="Premium annual price")
    parser.add_argument("--audience", default="Concrete Motivation supporters", help="Target audience")
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "outputs" / "membership"),
        help="Folder for generated membership files",
    )
    args = parser.parse_args()

    program = build_membership_program(
        offer=args.offer,
        monthly_price=args.monthly_price,
        annual_price=args.annual_price,
        premium_annual_price=args.premium_annual_price,
        audience=args.audience,
    )
    result = save_membership_program(program, output_dir=Path(args.output_dir))
    print(result.as_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

