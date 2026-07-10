#!/usr/bin/env python3
"""Show the Concrete Motivation CRM dashboard."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.crm_pipeline_manager import CRMPipelineManager


def main() -> int:
    parser = argparse.ArgumentParser(description="Show the Concrete Motivation CRM dashboard.")
    parser.add_argument(
        "--csv-path",
        default=str(ROOT / "outputs" / "crm" / "concrete_motivation_pipeline.csv"),
        help="Master CRM CSV path",
    )
    args = parser.parse_args()

    manager = CRMPipelineManager(csv_path=Path(args.csv_path))
    print(manager.dashboard_markdown())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

