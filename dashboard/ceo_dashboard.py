"""Command-line executive dashboard for Concrete Motivation."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dashboard.metrics import build_dashboard_metrics


def main() -> int:
    parser = argparse.ArgumentParser(description="Render the Concrete Motivation executive dashboard.")
    parser.add_argument(
        "--output",
        default=str(ROOT / "dashboard" / "metrics.md"),
        help="Path to write the dashboard report",
    )
    args = parser.parse_args()

    dashboard = build_dashboard_metrics(ROOT)
    rendered = dashboard.as_markdown().rstrip() + "\n"
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    print(f"Saved dashboard: {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

