"""Run the Concrete Motivation local system check."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.system_check import run_system_check


def main() -> int:
    result = run_system_check()
    print(result.as_markdown())
    return 0 if result.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
