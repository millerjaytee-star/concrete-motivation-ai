#!/usr/bin/env python
"""Verify championship launch readiness without external side effects."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from concrete_motivation.launch_system import verify_launch_system


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Print machine-readable JSON instead of Markdown.")
    args = parser.parse_args()

    report = verify_launch_system()
    print(report.as_json() if args.json else report.as_markdown())
    return 0 if report.overall_status in {"ready", "manual_action_required"} else 1


if __name__ == "__main__":
    raise SystemExit(main())
