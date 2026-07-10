#!/usr/bin/env python3
"""Create safe payment link configuration templates."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.payment_link_manager import PaymentLinkManager


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the Concrete Motivation payment link templates.")
    parser.add_argument(
        "--config-dir",
        default=str(ROOT / "config"),
        help="Folder for payment link templates",
    )
    args = parser.parse_args()

    config_dir = Path(args.config_dir)
    manager = PaymentLinkManager(
        config_path=config_dir / "payment_links.local.json",
        example_path=config_dir / "payment_links.example.json",
    )
    example = manager.create_example_config()
    local = manager.create_local_template()
    print(f"Saved example config: {example}")
    print(f"Saved local template: {local}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

