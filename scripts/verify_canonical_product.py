#!/usr/bin/env python3
"""Fail closed when repository release metadata does not identify canonical Lovable."""

from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "canonical-product.json"
EXPECTED = {
    "lovableProjectId": "09f0d02d-8d41-40c7-9c36-bbdbf8d11adf",
    "lovableProjectName": "concrete-motivation-app",
    "productionUrl": "https://concrete-motivation-app.lovable.app",
    "githubRepo": "millerjaytee-star/concrete-motivation-ai",
    "canonicalCommit": "f52ad32139ebffea6b413a475b4dd46dd5585b2c",
    "sourceOfTruth": "lovable",
}


def validate_config() -> list[str]:
    if not CONFIG.is_file():
        return [f"missing {CONFIG.relative_to(ROOT)}"]
    data = json.loads(CONFIG.read_text(encoding="utf-8"))
    errors = [f"{key}: expected {value!r}, got {data.get(key)!r}" for key, value in EXPECTED.items() if data.get(key) != value]
    if not data.get("lastVerifiedAt"):
        errors.append("lastVerifiedAt is required")
    return errors


def verify_live(url: str) -> list[str]:
    request = urllib.request.Request(url, headers={"User-Agent": "Concrete-Motivation-Release-Check/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            body = response.read(250_000).decode("utf-8", errors="replace")
            if response.status != 200:
                return [f"production returned HTTP {response.status}"]
            required = ["Concrete Motivation", "Built Under Pressure", "manifest.webmanifest"]
            return [f"production response missing {item!r}" for item in required if item not in body]
    except Exception as exc:  # network failures must be explicit, not silently passed
        return [f"production verification failed: {exc}"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="also verify the Lovable production response")
    args = parser.parse_args()
    errors = validate_config()
    if args.live and not errors:
        errors.extend(verify_live(EXPECTED["productionUrl"]))
    if errors:
        print("Canonical product verification FAILED")
        for error in errors:
            print(f"- {error}")
        return 1
    print("Canonical product verification PASSED")
    print(f"Source of truth: Lovable {EXPECTED['lovableProjectId']}")
    print(f"Production: {EXPECTED['productionUrl']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
