"""Compatibility launcher for the root Concrete Motivation command center."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from concrete_motivation.app import run


if __name__ == "__main__":
    run()
