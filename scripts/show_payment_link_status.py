#!/usr/bin/env python3
"""Show the Concrete Motivation payment link status."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.payment_link_manager import PaymentLinkManager


def main() -> int:
    parser = argparse.ArgumentParser(description="Show the Concrete Motivation payment link status.")
    parser.add_argument(
        "--config-dir",
        default=str(ROOT / "config"),
        help="Folder containing payment link templates",
    )
    args = parser.parse_args()

    config_dir = Path(args.config_dir)
    manager = PaymentLinkManager(
        config_path=config_dir / "payment_links.local.json",
        example_path=config_dir / "payment_links.example.json",
    )
    print(manager.status().as_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

