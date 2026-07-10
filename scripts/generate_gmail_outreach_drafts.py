#!/usr/bin/env python
"""Generate review-only Gmail outreach drafts from the outreach target list."""

from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TARGETS = ROOT / "outreach" / "qualified_outreach_targets.csv"
DRAFTS = ROOT / "outreach" / "generated_drafts.md"


def draft_for(row: dict[str, str]) -> str:
    segment = row["segment"].title()
    return f"""## {segment}: {row['who_to_help']}

**Fit signal:** {row['fit_signal']}
**Offer:** {row['offer']}
**Next step:** {row['next_step']}

Subject: Concrete Motivation support for {row['who_to_help']}

Hi [Name],

I am Jaytee Miller with Concrete Motivation. I help athletes, fathers, young people, teams, and leaders turn real pressure into discipline, ownership, and practical action.

I am reaching out because I noticed this fit signal: {row['fit_signal']}. I would like to explore whether {row['offer'].lower()} could serve your people in a real, measurable way.

Would you be open to a short conversation next week, or should I send a one-page outline first?

Jaytee Miller

**Safety:** Draft only. Do not send until Jaytee approves the contact and message.
"""


def main() -> int:
    rows = list(csv.DictReader(TARGETS.read_text(encoding="utf-8").splitlines()))
    body = ["# Generated Gmail Outreach Drafts", "", "These drafts are review-only. No email was sent.", ""]
    body.extend(draft_for(row) for row in rows)
    DRAFTS.write_text("\n".join(body).strip() + "\n", encoding="utf-8")
    print(f"Generated review-only drafts: {DRAFTS.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
