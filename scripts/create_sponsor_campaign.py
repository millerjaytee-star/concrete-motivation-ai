#!/usr/bin/env python3
"""Create a Concrete Motivation sponsor campaign."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.sponsorship_bot import SponsorshipBot


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a Concrete Motivation sponsorship campaign.")
    parser.add_argument("--segment", default="local gyms and barbershops", help="Sponsor segment")
    parser.add_argument("--audience", default="community partners and local brands", help="Audience")
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "outputs" / "sales_outreach" / "sponsorship"),
        help="Folder for generated campaign files",
    )
    args = parser.parse_args()

    result = SponsorshipBot(root=Path(args.output_dir)).run("Pressure Has a Purpose", args.audience, args.segment)
    print(result.as_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

