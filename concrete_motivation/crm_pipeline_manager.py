"""CRM pipeline manager for Concrete Motivation."""

from __future__ import annotations

import csv
import io
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from concrete_motivation.slugify import slugify


CRM_STAGES = (
    "New Lead",
    "Contacted",
    "Follow-Up Due",
    "Replied",
    "Meeting Requested",
    "Meeting Booked",
    "Proposal Sent",
    "Booked/Paid",
    "Nurture",
    "Closed/No Fit",
)

CRM_COLUMNS = (
    "lead_name",
    "organization",
    "contact_name",
    "role",
    "email",
    "phone",
    "segment",
    "offer",
    "stage",
    "last_contact_date",
    "next_follow_up_date",
    "source",
    "notes",
    "outcome",
)

CRM_PIPELINE_CSV = Path(__file__).resolve().parent.parent / "outputs" / "crm" / "concrete_motivation_pipeline.csv"
CRM_PIPELINE_FOLDER = Path(__file__).resolve().parent.parent / "outputs" / "crm" / "pipeline_manager"


@dataclass(frozen=True, slots=True)
class CRMLead:
    lead_name: str
    organization: str
    contact_name: str
    role: str
    email: str
    phone: str
    segment: str
    offer: str
    stage: str
    last_contact_date: str
    next_follow_up_date: str
    source: str
    notes: str
    outcome: str

    def as_dict(self) -> dict[str, str]:
        return {field: getattr(self, field) for field in CRM_COLUMNS}


@dataclass(frozen=True, slots=True)
class CRMPipelineResult:
    theme: str
    audience: str
    created_paths: tuple[Path, ...]

    def as_markdown(self) -> str:
        files = "\n".join(f"- {path}" for path in self.created_paths)
        return (
            "# CRM Pipeline Complete\n\n"
            f"**Theme:** {self.theme}\n\n"
            f"**Audience:** {self.audience}\n\n"
            "## Files Created\n"
            f"{files}"
        )


class CRMPipelineManager:
    """Create, append to, and summarize the Concrete Motivation CRM pipeline."""

    def __init__(self, root: Path | None = None, csv_path: Path | None = None) -> None:
        self.root = root or CRM_PIPELINE_FOLDER
        self.csv_path = csv_path or CRM_PIPELINE_CSV

    def run(self, theme: str = "Pressure Has a Purpose", audience: str = "core leads") -> CRMPipelineResult:
        clean_theme = theme.strip() or "Pressure Has a Purpose"
        clean_audience = audience.strip() or "core leads"
        stamp = datetime.now().astimezone().replace(microsecond=0).strftime("%Y-%m-%d-%H%M%S")
        folder = self.root / f"{stamp}-{slugify(clean_theme)}"
        folder.mkdir(parents=True, exist_ok=True)
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)

        self.ensure_pipeline_csv()

        files = {
            "00_crm_pipeline_overview.md": self._overview(clean_theme, clean_audience),
            "01_stage_tracking.md": self._stage_tracking(clean_theme, clean_audience),
            "02_follow_up_dates.csv": self._follow_up_dates(clean_theme, clean_audience),
            "03_pipeline_dashboard.md": self._pipeline_dashboard(clean_theme, clean_audience),
            "04_csv_export.csv": self._csv_export(clean_theme, clean_audience),
            "README.md": self._readme(clean_theme, clean_audience),
        }
        paths: list[Path] = []
        for filename, body in files.items():
            path = folder / filename
            path.write_text(body.strip() + "\n", encoding="utf-8")
            paths.append(path)
        return CRMPipelineResult(clean_theme, clean_audience, tuple(paths))

    def ensure_pipeline_csv(self) -> Path:
        """Create the master pipeline CSV when it is missing."""
        if self.csv_path.is_file():
            return self.csv_path
        self.csv_path.parent.mkdir(parents=True, exist_ok=True)
        self.csv_path.write_text(",".join(CRM_COLUMNS) + "\n", encoding="utf-8")
        return self.csv_path

    def load_leads(self) -> list[dict[str, str]]:
        if not self.csv_path.is_file():
            return []
        with self.csv_path.open(encoding="utf-8", newline="") as handle:
            return list(csv.DictReader(handle))

    def add_lead(self, lead: CRMLead) -> Path:
        """Append a lead row to the master pipeline CSV."""
        self.ensure_pipeline_csv()
        leads = self.load_leads()
        leads.append(lead.as_dict())
        self._write_master_rows(leads)
        return self.csv_path

    def dashboard_markdown(self) -> str:
        leads = self.load_leads()
        total = len(leads)
        pending = sum(1 for lead in leads if lead.get("stage", "").strip().lower() not in {"booked/paid", "closed/no fit"})
        scoreboard = (
            f"- Total leads: {total}",
            f"- Pending follow-ups: {pending}",
            f"- Active stages: {len(CRM_STAGES)}",
        )
        rows = "\n".join(f"| {lead.get('lead_name', '')} | {lead.get('stage', '')} | {lead.get('next_follow_up_date', '')} |" for lead in leads[:10])
        return f"""# CRM Dashboard

## Weekly Scoreboard
{chr(10).join(scoreboard)}

## Pipeline Snapshot
| Lead | Stage | Next Follow-Up |
|---|---|---|
{rows if rows else "| None | None | None |"}
"""

    def _readme(self, theme: str, audience: str) -> str:
        return f"""# CRM Pipeline Package

## Theme
{theme}

## Audience
{audience}

## Purpose
Track lead stage, follow-up dates, and next actions without losing momentum.

## Files
- CRM pipeline overview
- Stage tracking
- Follow-up dates CSV
- Pipeline dashboard
- CSV export
"""

    def _write_master_rows(self, rows: list[dict[str, str]]) -> None:
        with self.csv_path.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(CRM_COLUMNS))
            writer.writeheader()
            writer.writerows(rows)

    def _overview(self, theme: str, audience: str) -> str:
        return f"""# CRM Pipeline Overview

## Theme
{theme}

## Audience
{audience}

## Purpose
Track leads, follow-ups, meetings, proposals, and closed opportunities without losing momentum.
"""

    def _stage_tracking(self, theme: str, audience: str) -> str:
        rows = "\n".join(f"- {stage}" for stage in CRM_STAGES)
        return f"""# Stage Tracking

## Theme
{theme}

## Audience
{audience}

## Stages
{rows}

## Rules
- Every lead gets one stage.
- Every lead gets one next action.
- Every lead gets a follow-up date when needed.
"""

    def _follow_up_dates(self, theme: str, audience: str) -> str:
        today = datetime.now().astimezone().date()
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=["lead_name", "stage", "follow_up_date", "next_action", "notes"],
        )
        writer.writeheader()
        for index, stage in enumerate(("New Lead", "Contacted", "Follow-Up Due", "Replied")):
            writer.writerow(
                {
                    "lead_name": f"Lead {index + 1}",
                    "stage": stage,
                    "follow_up_date": (today).isoformat(),
                    "next_action": f"Follow up on {theme} for {audience}",
                    "notes": "",
                }
            )
        return buffer.getvalue()

    def _pipeline_dashboard(self, theme: str, audience: str) -> str:
        leads = self.load_leads()
        pending = sum(1 for lead in leads if lead.get("stage", "").strip().lower() not in {"booked/paid", "closed/no fit"})
        return f"""# Pipeline Dashboard

## Summary
- Theme: {theme}
- Audience: {audience}
- Total leads: {len(leads)}
- Pending follow-ups: {pending}

## Review Rhythm
- Check new leads daily.
- Review follow-up dates every morning.
- Move stale leads to nurture or closed/no fit weekly.
"""

    def _csv_export(self, theme: str, audience: str) -> str:
        buffer = io.StringIO()
        writer = csv.DictWriter(
            buffer,
            fieldnames=list(CRM_COLUMNS),
        )
        writer.writeheader()
        writer.writerow(
            CRMLead(
                lead_name="Lead 1",
                organization="School A",
                contact_name="",
                role="Athletic Director",
                email="",
                phone="",
                segment="school",
                offer="Speaking Session",
                stage="New Lead",
                last_contact_date="",
                next_follow_up_date="",
                source="CRM Pipeline Manager",
                notes=f"{theme} for {audience}",
                outcome="",
            ).as_dict()
        )
        writer.writerow(
            CRMLead(
                lead_name="Lead 2",
                organization="Sponsor B",
                contact_name="",
                role="Owner",
                email="",
                phone="",
                segment="sponsor",
                offer="Sponsorship",
                stage="Contacted",
                last_contact_date="",
                next_follow_up_date="",
                source="CRM Pipeline Manager",
                notes="",
                outcome="",
            ).as_dict()
        )
        writer.writerow(
            CRMLead(
                lead_name="Lead 3",
                organization="Podcast C",
                contact_name="",
                role="Host",
                email="",
                phone="",
                segment="podcast_guest",
                offer="Guest Interview",
                stage="Follow-Up Due",
                last_contact_date="",
                next_follow_up_date="",
                source="CRM Pipeline Manager",
                notes="",
                outcome="",
            ).as_dict()
        )
        return buffer.getvalue()
