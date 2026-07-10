"""CRM metrics for the Concrete Motivation executive dashboard."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class CRMMetrics:
    school_outreach_contacts: int
    sponsor_contacts: int
    podcast_guests: int
    pending_follow_ups: int

    def as_rows(self) -> tuple[tuple[str, str], ...]:
        return (
            ("School outreach contacts", str(self.school_outreach_contacts)),
            ("Sponsor contacts", str(self.sponsor_contacts)),
            ("Podcast guests", str(self.podcast_guests)),
            ("Pending follow-ups", str(self.pending_follow_ups)),
        )


def _csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _count_csv_rows(folder: Path, filename: str) -> int:
    if not folder.exists():
        return 0
    total = 0
    for path in folder.rglob(filename):
        total += len(_csv_rows(path))
    return total


def _count_pipeline_pending(csv_path: Path) -> int:
    if not csv_path.is_file():
        return 0
    with csv_path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    closed = {"booked/paid", "closed/no fit"}
    return sum(1 for row in rows if row.get("stage", "").strip().lower() not in closed)


def build_crm_metrics(root: Path | str | None = None) -> CRMMetrics:
    base = Path(root) if root is not None else Path(__file__).resolve().parent.parent
    outputs = base / "outputs"
    school = _count_csv_rows(outputs / "outreach_messages" / "school_outreach", "01_lead_template.csv")
    sponsor = _count_csv_rows(outputs / "sales_outreach" / "sponsorship", "01_sponsor_prospect_list_template.csv")
    podcast = _count_csv_rows(outputs / "podcast_production" / "guest_outreach", "01_guest_list.csv")
    pending = _count_pipeline_pending(outputs / "crm" / "concrete_motivation_pipeline.csv")

    return CRMMetrics(
        school_outreach_contacts=school,
        sponsor_contacts=sponsor,
        podcast_guests=podcast,
        pending_follow_ups=pending,
    )
