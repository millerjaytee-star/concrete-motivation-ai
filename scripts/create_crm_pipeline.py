#!/usr/bin/env python3
"""Create or reset the Concrete Motivation CRM pipeline package."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.crm_pipeline_manager import CRMPipelineManager


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the Concrete Motivation CRM pipeline.")
    parser.add_argument("--theme", default="Pressure Has a Purpose", help="CRM theme")
    parser.add_argument("--audience", default="core leads", help="CRM audience")
    parser.add_argument(
        "--csv-path",
        default=str(ROOT / "outputs" / "crm" / "concrete_motivation_pipeline.csv"),
        help="Master CRM CSV path",
    )
    parser.add_argument(
        "--output-dir",
        default=str(ROOT / "outputs" / "crm" / "pipeline_manager"),
        help="Folder for generated CRM package files",
    )
    args = parser.parse_args()

    manager = CRMPipelineManager(root=Path(args.output_dir), csv_path=Path(args.csv_path))
    result = manager.run(args.theme, args.audience)
    print(result.as_markdown())
    print(f"Saved master CSV: {manager.csv_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

