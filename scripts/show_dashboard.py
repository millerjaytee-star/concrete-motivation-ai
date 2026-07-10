#!/usr/bin/env python3
"""Show the Concrete Motivation executive dashboard."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dashboard.metrics import build_dashboard_metrics


def main() -> int:
    print(build_dashboard_metrics(ROOT).as_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

